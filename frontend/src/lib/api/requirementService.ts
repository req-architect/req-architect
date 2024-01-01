import fetchAPI from "./fetchAPI.ts";
import { Requirement } from "../../types.ts";

function getReqPrefix(reqId: string): string {
    // get all character without the last 3
    return reqId.slice(0, -3);
}

export async function fetchRequirements(
    docPrefix: string,
): Promise<Requirement[]> {
    return fetchAPI("GET", `/MyServer/req/?docId=${docPrefix}`);
}

export async function postRequirement(docPrefix: string) {
    if (!docPrefix) {
        throw new Error("docPrefix is empty");
    }
    await fetchAPI("POST", "/MyServer/req/", {
        docId: docPrefix,
        reqNumberId: "", // id assigned automatically
        reqText: "", // text is empty by default
    });
}

export async function putRequirement(reqId: string, reqText: string) {
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

export async function linkRequirement(req1Id: string, req2Id: string) {
    await fetchAPI("PUT", "/MyServer/req/link/", {
        req1Id,
        req2Id,
    });
}

export async function unlinkRequirement(req1Id: string, req2Id: string) {
    await fetchAPI("PUT", "/MyServer/req/unlink/", {
        req1Id,
        req2Id,
    });
}
