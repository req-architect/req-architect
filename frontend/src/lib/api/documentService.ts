import fetchAPI from "./fetchAPI.ts";
import { ReqDocumentWithChildren } from "../../types.ts";

/*
    This file contains functions to manage documents - functions to create, delete and fetch documents.
    It communicates with the backend through the fetchAPI function.
*/

export function postDocument(
    token_str: string,
    repositoryName: string,
    prefix: string,
    parent?: string,
) {
    return fetchAPI(token_str, repositoryName, "POST", "/api/doc/", {
        docId: prefix,
        ...(parent && { parentId: parent }),
    });
}

export function deleteDocument(
    tokenStr: string,
    repositoryName: string,
    prefix: string,
) {
    return fetchAPI(tokenStr, repositoryName, "DELETE", "/api/doc/", {
        docId: prefix,
    });
}

export function fetchDocuments(
    tokenStr: string,
    repositoryName: string,
): Promise<ReqDocumentWithChildren[]> {
    return fetchAPI(tokenStr, repositoryName, "GET", "/api/doc/");
}
