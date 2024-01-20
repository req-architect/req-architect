import fetchAPI from "./fetchAPI.ts";
import { AppUser } from "../../types.ts";

/* 
    This file contains a function to fetch the identity of the user.
*/

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
