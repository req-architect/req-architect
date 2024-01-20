import fetchAPI from "./fetchAPI.ts";
import { Requirement, RequirementWithDoc } from "../../types.ts";

/*
    This file contains functions to manage requirements.
    There are functions to create, delete, fetch, update, link, unlink or get all requirements or get the requirement prefix.
    It communicates with the backend through the fetchAPI function.
*/

function getReqPrefix(reqId: string): string {
    // get all character without the last 3
    return reqId.slice(0, -3);
}

export async function fetchRequirements(
    tokenStr: string,
    repositoryName: string,
    docPrefix: string,
): Promise<Requirement[]> {
    return fetchAPI(
        tokenStr,
        repositoryName,
        "GET",
        `/MyServer/req/?docId=${docPrefix}`,
    );
}

export async function postRequirement(
    tokenStr: string,
    repositoryName: string,
    docPrefix: string,
) {
    if (!docPrefix) {
        throw new Error("docPrefix is empty");
    }
    await fetchAPI(tokenStr, repositoryName, "POST", "/MyServer/req/", {
        docId: docPrefix,
        reqNumberId: "", // id assigned automatically
        reqText: "", // text is empty by default
    });
}

export async function putRequirement(
    tokenStr: string,
    repositoryName: string,
    reqId: string,
    reqText: string,
) {
    const prefix = getReqPrefix(reqId);
    await fetchAPI(tokenStr, repositoryName, "PUT", "/MyServer/req/", {
        docId: prefix,
        reqId,
        reqText,
    });
}
export async function deleteRequirement(
    tokenStr: string,
    repositoryName: string,
    reqId: string,
) {
    const prefix = getReqPrefix(reqId);
    await fetchAPI(tokenStr, repositoryName, "DELETE", "/MyServer/req/", {
        docId: prefix,
        reqId,
    });
}

export async function linkRequirement(
    tokenStr: string,
    repositoryName: string,
    req1Id: string,
    req2Id: string,
) {
    await fetchAPI(tokenStr, repositoryName, "PUT", "/MyServer/req/link/", {
        req1Id,
        req2Id,
    });
}

export async function unlinkRequirement(
    tokenStr: string,
    repositoryName: string,
    req1Id: string,
    req2Id: string,
) {
    await fetchAPI(tokenStr, repositoryName, "PUT", "/MyServer/req/unlink/", {
        req1Id,
        req2Id,
    });
}

export async function getAllRequirements(
    tokenStr: string,
    repositoryName: string,
): Promise<RequirementWithDoc[]> {
    return fetchAPI(tokenStr, repositoryName, "GET", "/MyServer/req/all");
}
