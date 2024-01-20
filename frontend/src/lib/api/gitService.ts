import fetchAPI from "./fetchAPI.ts";

/*
    This file contains functions to manage git repositories - functions to post commits, get repositories and post chosen repository.
    It communicates with the backend through the fetchAPI function.
*/

type ResponseCommit = {
    message: string;
};

export async function postCommit(
    tokenStr: string,
    repositoryName: string,
    commitText: string,
): Promise<ResponseCommit> {
    return await fetchAPI(
        tokenStr,
        repositoryName,
        "POST",
        "/MyServer/git/commit/",
        {
            commitText: commitText,
        },
    );
}

export async function getRepos(tokenStr: string): Promise<string[]> {
    const response = await fetchAPI(
        tokenStr,
        null,
        "GET",
        "/MyServer/git/repos/",
    );
    return await response;
}

export async function postRepo(tokenStr: string, repositoryName: string) {
    return await fetchAPI(
        tokenStr,
        repositoryName,
        "POST",
        "/MyServer/git/repos/",
        {},
    );
}
