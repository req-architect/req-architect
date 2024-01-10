import fetchAPI from "./fetchAPI.ts";


export async function postCommit(commitText: string) {
    // await fetchAPI("POST", "/MyServer/doc/", {
    //     docId: prefix,
    //     ...(parent && { parentId: parent }),
    // });
    console.log("Commit Text: " + commitText);
}