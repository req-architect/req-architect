import fetchAPI from "./fetchAPI.ts";
import { AppUser } from "../../types.ts";

export function fetchIdentity(
    abortController: AbortController,
): Promise<AppUser> {
    return fetchAPI("GET", "/MyServer/identity/", undefined, abortController);
}
