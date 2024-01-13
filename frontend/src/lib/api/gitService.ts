import fetchAPI from "./fetchAPI.ts";

type ResponseCommit = {
    message: string;
};

export async function postCommit(commitText: string): Promise<ResponseCommit> {
    return await fetchAPI("POST", "/MyServer/git/commit/", {
        commitText: commitText,
    });
}

export async function getRepos(): Promise<string[]> {
    const response = await fetchAPI("GET", "/MyServer/git/repos/");
    return await response;
}

export async function postRepo() {
    return await fetchAPI("POST", "/MyServer/git/repos/", {});
}
