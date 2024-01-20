/* 
This module tests service API functionalities for browser app-server communication.
*/
import { test, describe, beforeEach, afterEach } from "@jest/globals";
import { GenericContainer, StartedTestContainer } from "testcontainers";
// import { fetchIdentity } from "../../lib/api/authService.ts";
import { getRepos, postRepo, postCommit } from "../../lib/api/gitService";
import {
    fetchDocuments,
    postDocument,
    deleteDocument,
} from "../../lib/api/documentService";
import {
    fetchRequirements,
    postRequirement,
    deleteRequirement,
    linkRequirement,
    unlinkRequirement,
    putRequirement,
    getAllRequirements,
} from "../../lib/api/requirementService";
import { APIError } from "../../lib/api/fetchAPI";

const TEST_TOKEN = "test_token";
const TEST_REPOS = ["test_repo_1", "test_repo_2"];

let TEST_API_URL = "http://localhost:8000";

function constant(constant: string) {
    constant;
    return TEST_API_URL;
}

jest.mock("../../constants.ts", () => {
    return {
        constant,
    };
});

describe("GitServiceTest", () => {
    let container: StartedTestContainer;
    beforeEach(async () => {
        const genericContainer =
            await GenericContainer.fromDockerfile("../backend").build();
        container = await genericContainer
            .withExposedPorts(8000)
            .withEnvironment({
                CORS_ALLOWED_ORIGINS: "http://localhost:3000",
                REPOS_FOLDER: "/repos",
                SERVER_TEST_MODE: "1",
            })
            .start();
        TEST_API_URL = `http://${container.getHost()}:${container.getMappedPort(
            8000,
        )}`;
    }, 120000);

    afterEach(async () => {
        await container.stop();
    });

    test("testGetRepos", async () => {
        const repos = await getRepos(TEST_TOKEN);
        expect(repos).toEqual(TEST_REPOS);
    }, 120000);

    test("testPostRepo", async () => {
        const response = await postRepo(TEST_TOKEN, TEST_REPOS[0]);
        expect(response.message).toBe("OK");
    }, 120000);

    test("testPostCommit", async () => {
        const response = await postCommit(
            TEST_TOKEN,
            TEST_REPOS[0],
            "Some commit text",
        );
        expect(response.message).toBe(
            "Successfully staged changes in repository!",
        );
    }, 120000);
});

describe("documentServiceTest", () => {
    let container: StartedTestContainer;
    beforeEach(async () => {
        const genericContainer =
            await GenericContainer.fromDockerfile("../backend").build();
        container = await genericContainer
            .withExposedPorts(8000)
            .withEnvironment({
                CORS_ALLOWED_ORIGINS: "http://localhost:3000",
                REPOS_FOLDER: "/repos",
                SERVER_TEST_MODE: "1",
            })
            .start();
        TEST_API_URL = `http://${container.getHost()}:${container.getMappedPort(
            8000,
        )}`;
    }, 120000);

    afterEach(async () => {
        await container.stop();
    });

    test("testFetchDocuments", async () => {
        await postRepo(TEST_TOKEN, TEST_REPOS[0]);
        const docs = await fetchDocuments(TEST_TOKEN, TEST_REPOS[0]);
        expect(docs).toEqual([]);
    }, 120000);

    test("testPostDocument", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        const docs = await fetchDocuments(TEST_TOKEN, repo);
        expect(docs.length).toBe(1);
        expect(docs[0].prefix).toBe("root");
        expect(docs[0].children).toEqual([]);
    }, 120000);

    test("ERRORtestPostDocument-multipleRoots", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        try {
            await postDocument(TEST_TOKEN, repo, "root2");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("NO_PARENT_SPECIFIED");
    }, 120000);

    test("ERRORtestPostDocument-parentOfEmptyTree", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);
        try {
            await postDocument(TEST_TOKEN, repo, "SYSREQ", "root");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe(
            "PARENT_OF_EMPTY_TREE_SPECIFIED",
        );
    }, 120000);

    test("testPostDocumentWithParent", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postDocument(TEST_TOKEN, repo, "SYSREQ", "root");
        const docs = await fetchDocuments(TEST_TOKEN, repo);

        expect(docs.length).toBe(1);
        expect(docs[0].prefix).toBe("root");
        const children = docs[0].children;
        expect(children).toBeTruthy();
        if (!children) return;
        expect(children.length).toBe(1);
        expect(children[0].prefix).toBe("SYSREQ");
        expect(children[0].children).toEqual([]);
    }, 120000);

    test("testDeleteDocument", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await deleteDocument(TEST_TOKEN, repo, "root");

        const docs = await fetchDocuments(TEST_TOKEN, repo);
        expect(docs).toEqual([]);
    }, 120000);

    test("ERRORtestPostExistingDocument", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        try {
            await postDocument(TEST_TOKEN, repo, "root", "root");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("DOCUMENT_ALREADY_EXISTS");
    }, 120000);

    test("testDeleteWithChildren", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postDocument(TEST_TOKEN, repo, "SYSREQ", "root");
        await deleteDocument(TEST_TOKEN, repo, "root");

        const docs = await fetchDocuments(TEST_TOKEN, repo);
        expect(docs).toEqual([]);
    }, 120000);

    test("ERRORtestDeleteDocument-NoDocumentYet", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);
        try {
            await deleteDocument(TEST_TOKEN, repo, "root");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("NO_DOCUMENTS");
    }, 120000);

    test("ERRORtestDeleteDocument-NoSuchDocument", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        try {
            await deleteDocument(TEST_TOKEN, repo, "SYSREQ");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("DOC_NOT_FOUND");
    }, 120000);
});

describe("ReqServiceTest", () => {
    let container: StartedTestContainer;
    beforeEach(async () => {
        const genericContainer =
            await GenericContainer.fromDockerfile("../backend").build();
        container = await genericContainer
            .withExposedPorts(8000)
            .withEnvironment({
                CORS_ALLOWED_ORIGINS: "http://localhost:3000",
                REPOS_FOLDER: "/repos",
                SERVER_TEST_MODE: "1",
            })
            .start();
        TEST_API_URL = `http://${container.getHost()}:${container.getMappedPort(
            8000,
        )}`;
    }, 120000);

    afterEach(async () => {
        await container.stop();
    });

    test("testFetchRequirements", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");

        const reqs = await fetchRequirements(TEST_TOKEN, repo, "root");
        expect(reqs).toEqual([]);
    }, 120000);

    test("ERRORtestFetchRequirements-NoSuchDocument", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);

        try {
            await fetchRequirements(TEST_TOKEN, repo, "root");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("DOC_NOT_FOUND");
    }, 120000);

    test("testGetAllRequirements", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postDocument(TEST_TOKEN, repo, "SYSREQ", "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "SYSREQ");

        const reqs = await getAllRequirements(TEST_TOKEN, repo);
        expect(reqs.length).toBe(3);
        const root001 = reqs[0];
        const root002 = reqs[1];
        const SYSREQ001 = reqs[2];
        expect(root001.id).toBe("root001");
        expect(root001.docPrefix).toBe("root");
        expect(root002.id).toBe("root002");
        expect(root002.docPrefix).toBe("root");
        expect(SYSREQ001.id).toBe("SYSREQ001");
        expect(SYSREQ001.docPrefix).toBe("SYSREQ");
    }, 120000);

    test("testAddRequirement", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");

        const reqs = await fetchRequirements(TEST_TOKEN, repo, "root");
        expect(reqs.length).toBe(1);
        const req = reqs[0];
        expect(req.id).toBe("root001");
        expect(req.text).toBe("");
        expect(req.links).toEqual([]);
        expect(req.reviewed).toBe(false);
    }, 120000);

    test("ERRORtestAddRequirement-noSuchDocument", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);

        try {
            await postRequirement(TEST_TOKEN, repo, "root");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("DOC_NOT_FOUND");
    }, 120000);

    test("testDeleteRequirement", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await deleteRequirement(TEST_TOKEN, repo, "root001");

        const reqs = await fetchRequirements(TEST_TOKEN, repo, "root");
        expect(reqs.length).toBe(0);
    }, 120000);

    test("ERRORtestDeleteRequirement-IncorrectRequirementId", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        try {
            await deleteRequirement(TEST_TOKEN, repo, "root001");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("REQ_NOT_FOUND");
    }, 120000);

    test("ERRORtestDeleteRequirement-IncorrectDocumentId", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        try {
            await deleteRequirement(TEST_TOKEN, repo, "SYSREQ001");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("REQ_NOT_FOUND");
    }, 120000);

    test("testDeleteRequirement-MultipleReqsInRepo", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await deleteRequirement(TEST_TOKEN, repo, "root001");

        const reqs = await fetchRequirements(TEST_TOKEN, repo, "root");
        expect(reqs.length).toBe(1);
        const req = reqs[0];
        expect(req.id).toBe("root002");
    }, 120000);

    test("testDeleteDeletedDocumentReqs", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await deleteDocument(TEST_TOKEN, repo, "root");

        const reqs = await getAllRequirements(TEST_TOKEN, repo);
        expect(reqs.length).toBe(0);
    }, 120000);

    test("testDeleteDeletedDocumentReqs-multipleDocumentsInRepo", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postDocument(TEST_TOKEN, repo, "SYSREQ", "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "SYSREQ");
        await deleteDocument(TEST_TOKEN, repo, "SYSREQ");

        const reqs = await getAllRequirements(TEST_TOKEN, repo);
        expect(reqs.length).toBe(1);
        const req = reqs[0];
        expect(req.docPrefix).toBe("root");
    }, 120000);

    test("testPutRequirement", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await putRequirement(
            TEST_TOKEN,
            repo,
            "root001",
            "Some requirement text",
        );

        const reqs = await fetchRequirements(TEST_TOKEN, repo, "root");
        expect(reqs[0].text).toBe("Some requirement text");
    }, 120000);

    test("ERRORtestPutRequirement-noSuchRequirement", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        try {
            await putRequirement(TEST_TOKEN, repo, "root001", "");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("REQ_NOT_FOUND");
    }, 120000);

    test("testLinkRequirement", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await linkRequirement(TEST_TOKEN, repo, "root001", "root002");

        const reqs = await fetchRequirements(TEST_TOKEN, repo, "root");
        const root001 = reqs[0];
        const root002 = reqs[1];
        expect(root001.links).toEqual(["root002"]);
        expect(root002.links).toEqual([]);
    }, 120000);

    test("ERRORtestLinkRequirement-makeCycle", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await linkRequirement(TEST_TOKEN, repo, "root001", "root002");
        try {
            await linkRequirement(TEST_TOKEN, repo, "root002", "root001");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("LINK_CYCLE_ATTEMPT");
    }, 120000);

    test("ERRORtestLinkRequirement-makeCycle-MoreThanOneReqInCycle", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await linkRequirement(TEST_TOKEN, repo, "root001", "root002");
        await linkRequirement(TEST_TOKEN, repo, "root002", "root003");
        try {
            await linkRequirement(TEST_TOKEN, repo, "root003", "root001");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("LINK_CYCLE_ATTEMPT");
    }, 120000);

    test("testUnlinkRequirement", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        await linkRequirement(TEST_TOKEN, repo, "root001", "root002");
        await unlinkRequirement(TEST_TOKEN, repo, "root001", "root002");

        const reqs = await fetchRequirements(TEST_TOKEN, repo, "root");
        const root001 = reqs[0];
        const root002 = reqs[1];
        expect(root001.links).toEqual([]);
        expect(root002.links).toEqual([]);
    }, 120000);

    test("ERRORtestUnlinkRequirement-NoSuchRequirement", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        try {
            await unlinkRequirement(TEST_TOKEN, repo, "root001", "root002");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("REQ_NOT_FOUND");
    }, 120000);

    test("ERRORtestUnlinkRequirement-NoSuchRequirement-v2", async () => {
        const repo = TEST_REPOS[0];
        let error;
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postRequirement(TEST_TOKEN, repo, "root");
        try {
            await unlinkRequirement(TEST_TOKEN, repo, "root002", "root001");
        } catch (err) {
            error = err;
        }
        expect(error).toBeInstanceOf(APIError);
        const castedError = error as APIError;
        expect(castedError.api_error_code).toBe("REQ_NOT_FOUND");
    }, 120000);
});
