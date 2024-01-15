import { useNavigate } from "react-router-dom";
import { useAuth } from "./useAuthContext.ts";
import { useEffect } from "react";

export default function useLoginRedirect(value: boolean, dest: string) {
    const navigate = useNavigate();
    const authTools = useAuth();
    useEffect(() => {
        if (authTools.isLoggedIn() === value) {
            navigate(dest);
            return;
        }
    }, [dest, value, authTools, navigate]);
}
