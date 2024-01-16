import fetchAPI from "./fetchAPI.ts";
import { AppUser } from "../../types.ts";

export function fetchIdentity(
    tokenStr: string,
    abortController: AbortController,
): Promise<AppUser> {
    return fetchAPI(
        tokenStr,
        null,
        "GET",
        "/MyServer/identity/",
        undefined,
        abortController,
    );
}
