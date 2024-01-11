import { getLocalStorageObject } from "../localStorageUtil.ts";
import fetchAPI from "./fetchAPI.ts";

export async function postCommit(commitText: string) {
    // console.log("Commit Text: " + commitText);
    await fetchAPI("POST", "/MyServer/git/commit/", {
        commitText: commitText,
    });
    // console.log("Server replied: " + response.message);
}

export async function getRepos(): Promise<string[]> {
    const response = await fetchAPI("GET", "/MyServer/git/repos/");
    return await response;
}

export async function postRepo(): Promise<string> {
    return await fetchAPI("POST", "/MyServer/git/repos/", {});
}
