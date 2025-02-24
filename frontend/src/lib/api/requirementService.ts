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

export function fetchRequirements(
    tokenStr: string,
    repositoryName: string,
    docPrefix: string,
): Promise<Requirement[]> {
    return fetchAPI(
        tokenStr,
        repositoryName,
        "GET",
        `/api/req/?docId=${docPrefix}`,
    );
}

export function postRequirement(
    tokenStr: string,
    repositoryName: string,
    docPrefix: string,
) {
    if (!docPrefix) {
        throw new Error("docPrefix is empty");
    }
    return fetchAPI(tokenStr, repositoryName, "POST", "/api/req/", {
        docId: docPrefix,
        reqNumberId: "", // id assigned automatically
        reqText: "", // text is empty by default
    });
}

export function putRequirement(
    tokenStr: string,
    repositoryName: string,
    reqId: string,
    reqText: string,
) {
    const prefix = getReqPrefix(reqId);
    return fetchAPI(tokenStr, repositoryName, "PUT", "/api/req/", {
        docId: prefix,
        reqId,
        reqText,
    });
}
export function deleteRequirement(
    tokenStr: string,
    repositoryName: string,
    reqId: string,
) {
    const prefix = getReqPrefix(reqId);
    return fetchAPI(tokenStr, repositoryName, "DELETE", "/api/req/", {
        docId: prefix,
        reqId,
    });
}

export function linkRequirement(
    tokenStr: string,
    repositoryName: string,
    req1Id: string,
    req2Id: string,
) {
    return fetchAPI(tokenStr, repositoryName, "PUT", "/api/req/link/", {
        req1Id,
        req2Id,
    });
}

export function unlinkRequirement(
    tokenStr: string,
    repositoryName: string,
    req1Id: string,
    req2Id: string,
) {
    return fetchAPI(tokenStr, repositoryName, "PUT", "/api/req/unlink/", {
        req1Id,
        req2Id,
    });
}

export function getAllRequirements(
    tokenStr: string,
    repositoryName: string,
): Promise<RequirementWithDoc[]> {
    return fetchAPI(tokenStr, repositoryName, "GET", "/api/req/all");
}
