import fetchAPI from "./fetchAPI.ts";
import { Requirement } from "../../types.ts";

function getReqPrefix(reqId: string): string {
    // get all characters to first digit
    const prefix = reqId.match(/^[^\d]+/);
    if (prefix === null) {
        throw new Error("Invalid requirement ID");
    }
    return prefix[0];
}

export async function fetchRequirements(
    docPrefix: string,
): Promise<Requirement[]> {
    return fetchAPI("GET", `/MyServer/req/?docId=${docPrefix}`);
}

export async function postRequirement(docPrefix: string) {
    if (!docPrefix){
        alert("To add a requirement you must first choose a document");
        return;
    }
    await fetchAPI("POST", "/MyServer/req/", {
        docId: docPrefix,
        reqNumberId: "", // id assigned automatically
        reqText: "", // text is empty by default
    });
}

export async function putRequirement(reqId: string, reqText: string) {
    console.log(`Updating ${reqId} to ${reqText}`);
    const prefix = getReqPrefix(reqId);
    await fetchAPI("PUT", "/MyServer/req/", {
        docId: prefix,
        reqId,
        reqText,
    });
}
export async function deleteRequirement(reqId: string) {
    const prefix = getReqPrefix(reqId);
    await fetchAPI("DELETE", "/MyServer/req/", {
        docId: prefix,
        reqId,
    });
}
