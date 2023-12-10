import fetchAPI from "./fetchAPI.ts";
import { Requirement } from "../types.ts";

export async function fetchRequirements(
    docPrefix: string,
): Promise<Requirement[]> {
    return fetchAPI("GET", `/MyServer/req/?docId=${docPrefix}`);
}
