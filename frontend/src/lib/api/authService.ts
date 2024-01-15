import fetchAPI from "./fetchAPI.ts";
import { AppUser } from "../../types.ts";

export function fetchIdentity(): Promise<AppUser> {
    return fetchAPI("GET", "/MyServer/identity/");
}
