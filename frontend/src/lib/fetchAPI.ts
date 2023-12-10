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

export default function fetchAPI(method: Method, uri: string, body?: object) {
    return fetch(`${import.meta.env.VITE_APP_API_URL}${uri}`, {
        method,
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    })
        .then(async (response) => {
            if (!response.ok) {
                const data = await response.json().catch(() => {
                    throw new APIError("Unknown error", response.status);
                });
                if (data.message) {
                    throw new APIError(data.message, response.status);
                } else {
                    throw new APIError("Unknown error", response.status);
                }
            }
            return response.json();
        })
        .catch((error) => {
            if (error instanceof APIError) {
                toast.error(error.message);
            }
            throw error;
        });
}
