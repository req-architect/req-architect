import { useNavigate } from "react-router-dom";
import { useAuth } from "./useAuthContext.ts";
import { useEffect } from "react";

/*
    This hook is used to redirect the user to a specific page if they are logged in/out.
    It is used to redirect the user to the home page if they are logged in and to the login page if they are logged out.
*/

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
