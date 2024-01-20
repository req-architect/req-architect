import fetchAPI from "./fetchAPI.ts";
import { ReqDocumentWithChildren } from "../../types.ts";

/* 
    This file contains functions to manage documents - functions to create, delete and fetch documents.
    It communicates with the backend through the fetchAPI function.
*/

export async function postDocument(
    token_str: string,
    repositoryName: string,
    prefix: string,
    parent?: string,
) {
    await fetchAPI(token_str, repositoryName, "POST", "/MyServer/doc/", {
        docId: prefix,
        ...(parent && { parentId: parent }),
    });
}

export async function deleteDocument(
    tokenStr: string,
    repositoryName: string,
    prefix: string,
) {
    await fetchAPI(tokenStr, repositoryName, "DELETE", "/MyServer/doc/", {
        docId: prefix,
    });
}

export async function fetchDocuments(
    tokenStr: string,
    repositoryName: string,
): Promise<ReqDocumentWithChildren[]> {
    return fetchAPI(tokenStr, repositoryName, "GET", "/MyServer/doc/");
}
