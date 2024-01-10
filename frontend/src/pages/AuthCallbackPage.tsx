import { useEffect, useState } from "react";
import { JWTToken } from "../types.ts";
import { setLocalStorageObject } from "../lib/localStorageUtil.ts";
import { useNavigate } from "react-router-dom";

export default function AuthCallbackPage() {
    const [error, setError] = useState<boolean>(false);
    const navigate = useNavigate();
    useEffect(() => {
        const url = new URL(window.location.href);
        const token = url.searchParams.get("token");
        const exp = url.searchParams.get("exp");
        const iat = url.searchParams.get("iat");
        if (!(token && exp && iat)) {
            setError(true);
            return;
        }
        setLocalStorageObject("jwtToken", {
            token: token,
            exp: parseInt(exp),
            iat: parseInt(iat),
        } as JWTToken);
        navigate("/main_page");
    }, [navigate]);
    return error ? <div>Something went wrong</div> : <></>;
}
