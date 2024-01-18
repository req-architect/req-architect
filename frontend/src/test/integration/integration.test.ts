import { test, describe, beforeEach, afterEach } from "@jest/globals";
import { GenericContainer, StartedTestContainer } from "testcontainers";
import { fetchIdentity } from "../../lib/api/authService.ts";

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
    }, 60000);

    afterEach(async () => {
        await container.stop();
    });
    test("healthcheck", async () => {
        const port = container.getMappedPort(8000);
        const host = container.getHost();
        const response = await fetch(`http://${host}:${port}/healthcheck`);
        expect(response.status).toBe(200);
        const text = await response.text();
        expect(text).toBe("OK");
    }, 60000);
    test("test", async () => {
        fetchIdentity("test", new AbortController());
    });
});
