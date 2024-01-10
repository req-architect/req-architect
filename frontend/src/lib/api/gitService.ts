import fetchAPI from "./fetchAPI.ts";


export async function postCommit(commitText: string) {
    // console.log("Commit Text: " + commitText);
    await fetchAPI("POST", "/MyServer/git/commit/", {
        commitText: commitText,
    });
    // console.log("Server replied: " + response.message);
}