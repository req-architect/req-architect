import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuthContext.ts";
import useLoginRedirect from "../hooks/useLoginRedirect.ts";

export default function AuthCallbackPage() {
    const [error, setError] = useState<boolean>(false);
    const authTools = useAuth();
    const { login } = authTools;
    useLoginRedirect(true, "/repo");
    useEffect(() => {
        const url = new URL(window.location.href);
        const token = url.searchParams.get("token");
        const exp = url.searchParams.get("exp");
        const iat = url.searchParams.get("iat");
        if (!(token && exp && iat)) {
            setError(true);
            return;
        }
        login({
            token: token,
            exp: parseInt(exp),
            iat: parseInt(iat),
        });
    }, [login]);
    return error ? <div>Something went wrong</div> : <></>;
}
