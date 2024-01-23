import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuthContext.ts";
import useLoginRedirect from "../hooks/useLoginRedirect.ts";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

/*
    This page is used to handle the callback from the authentication server.
    It will extract the token and expiration date from the URL and store it in the auth context.
    It will then (if everything went ok) redirect the user to the repo page.
*/

export default function AuthCallbackPage() {
    const [error, setError] = useState<boolean>(false);
    const authTools = useAuth();
    const navigate = useNavigate();
    const { login } = authTools;
    useLoginRedirect(true, "/repo");
    useEffect(() => {
        const url = new URL(window.location.href);
        const token = url.searchParams.get("token");
        const exp = url.searchParams.get("exp");
        const iat = url.searchParams.get("iat");
        const message = url.searchParams.get("message");
        const api_error_code = url.searchParams.get("api_error_code");
        if (message && api_error_code) {
            toast.error(message);
            navigate("/login");
            return;
        }
        if (!(token && exp && iat)) {
            setError(true);
            return;
        }
        login({
            token: token,
            exp: parseInt(exp),
            iat: parseInt(iat),
        });
    }, [login, navigate]);
    return error ? <div>Something went wrong</div> : <></>;
}
