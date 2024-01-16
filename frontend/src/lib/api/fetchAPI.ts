import { toast } from "react-toastify";

type Method = "GET" | "POST" | "PUT" | "DELETE";

export class APIError extends Error {
    constructor(
        message: string,
        public status: number,
    ) {
        super(message);
    }
}

export enum CUSTOM_ERROR_MESSAGES {
    link_cycle_attempt = "could not build document tree",
}

export default function fetchAPI(
    tokenStr: string,
    repositoryName: string | null,
    method: Method,
    uri: string,
    body?: object,
    abortController?: AbortController,
) {
    if (repositoryName) {
        if (uri.includes("?")) {
            uri = uri + "&repositoryName=" + repositoryName;
        } else {
            uri = uri + "?repositoryName=" + repositoryName;
        }
    }
    return fetch(`${import.meta.env.VITE_APP_API_URL}${uri}`, {
        method,
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${tokenStr}`,
        },
        body: JSON.stringify(body),
        signal: abortController?.signal,
    })
        .then(async (response) => {
            if (!response.ok) {
                const data = await response.json().catch(() => {
                    throw new APIError(response.statusText, response.status);
                });
                if (data.message) {
                    throw new APIError(data.message, response.status);
                } else {
                    throw new APIError(response.statusText, response.status);
                }
            }
            return response.json();
        })
        .catch((error) => {
            if (
                error instanceof APIError &&
                !(
                    error.status === 409 &&
                    error.message.includes(
                        CUSTOM_ERROR_MESSAGES.link_cycle_attempt,
                    )
                )
            ) {
                console.log(error);
                toast.error(error.message);
            }
            throw error;
        });
}
