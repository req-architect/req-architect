import { test, describe, beforeEach, afterEach } from "@jest/globals";
import { GenericContainer, StartedTestContainer } from "testcontainers";
// import { fetchIdentity } from "../../lib/api/authService.ts";
import { getRepos, postRepo, postCommit } from "../../lib/api/gitService";
import { fetchDocuments, postDocument, deleteDocument } from "../../lib/api/documentService";

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

describe("integration tests", () => {
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
    // test("healthcheck", async () => {
    //     const port = container.getMappedPort(8000);
    //     const host = container.getHost();
    //     const response = await fetch(`http://${host}:${port}/healthcheck`);
    //     expect(response.status).toBe(200);
    //     const text = await response.text();
    //     expect(text).toBe("OK");
    // }, 120000);

    test("testGetRepos", async () => {
        const repos = await getRepos(TEST_TOKEN);
        expect(repos).toEqual(TEST_REPOS);
    }, 120000);

    test("testPostRepo", async () => {
        const response = await postRepo(TEST_TOKEN, TEST_REPOS[0]);
        expect(response.message).toBe("OK");
    }, 120000);

    test("testPostCommit", async () => {
        const response = await postCommit(TEST_TOKEN, TEST_REPOS[0], "Some commit text");
        expect(response.message).toBe("Successfully staged changes in repository!");
    }, 120000);

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

    test("testPostDocumentWithParent", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await postDocument(TEST_TOKEN, repo, "SYSREQ", "root");
        const docs = await fetchDocuments(TEST_TOKEN, repo);

        expect(docs.length).toBe(1);
        expect(docs[0].prefix).toBe("root");
        const children = docs[0].children;
        if (children) {
            expect(children.length).toBe(1);
            expect(children[0].prefix).toBe("SYSREQ");
            expect(children[0].children).toEqual([]);
        }
    }, 120000);

    test("testDeleteDocument", async () => {
        const repo = TEST_REPOS[0];
        await postRepo(TEST_TOKEN, repo);
        await postDocument(TEST_TOKEN, repo, "root");
        await deleteDocument(TEST_TOKEN, repo, "root");

        const docs = await fetchDocuments(TEST_TOKEN, repo);
        expect(docs).toEqual([]);
    }, 120000);
});
