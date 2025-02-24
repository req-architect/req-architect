import fetchAPI from "./fetchAPI.ts";

/*
    This file contains functions to manage git repositories - functions to post commits, get repositories and post chosen repository.
    It communicates with the backend through the fetchAPI function.
*/

export function postCommit(
    tokenStr: string,
    repositoryName: string,
    commitText: string,
) {
    return fetchAPI(tokenStr, repositoryName, "POST", "/api/git/commit/", {
        commitText: commitText,
    });
}

export function getRepos(tokenStr: string): Promise<string[]> {
    return fetchAPI(tokenStr, null, "GET", "/api/git/repos/");
}

export function postRepo(tokenStr: string, repositoryName: string) {
    return fetchAPI(
        tokenStr,
        repositoryName,
        "POST",
        "/api/git/repos/",
        {},
    );
}
