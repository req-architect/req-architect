import fetchAPI from "./fetchAPI.ts";
import { ReqDocumentWithChildren } from "../../types.ts";

export async function postDocument(prefix: string, parent?: string) {
    await fetchAPI("POST", "/MyServer/doc/", {
        docId: prefix,
        ...(parent && { parentId: parent }),
    });
}

export async function deleteDocument(prefix: string) {
    await fetchAPI("DELETE", "/MyServer/doc/", {
        docId: prefix,
    });
}

export async function fetchDocuments(): Promise<ReqDocumentWithChildren[]> {
    return fetchAPI("GET", "/MyServer/doc/");
}
