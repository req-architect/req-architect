import { useLocalStorage } from "usehooks-ts";
import { AppUser, JWTToken } from "../types.ts";
import { useCallback, useContext, useEffect, useState } from "react";
import { fetchIdentity } from "../lib/api/authService.ts";
import { AuthContext } from "../App.tsx";
import { toast } from "react-toastify";
import { APIError } from "../lib/api/fetchAPI.ts";

/*
    This hook is used to manage the authentication state of the user.
    It is used to login/logout the user and to check if the user is logged in.
    It also provides the user object and the token string.
*/

export type AuthContextTools = {
    tokenStr: string | null;
    user: AppUser | null;
    initialLoading: boolean;
    logout: (reason?: string) => void;
    login: (token: JWTToken) => void;
    isLoggedIn: () => boolean | null;
};

type AuthState = {
    user: AppUser | null;
    initialLoading: boolean;
};

export default function useAuthContext() {
    const [token, setToken] = useLocalStorage<JWTToken>("jwtToken", null);
    const [authState, setAuthState] = useState<AuthState>({
        user: null,
        initialLoading: true,
    });
    const logout = useCallback(
        (reason: string = "") => {
            setToken(null);
            if (reason) toast.info(`You have been logged out: ${reason}`);
            else toast.info(`You have been logged out`);
        },
        [setToken],
    );
    useEffect(() => {
        const abortController = new AbortController();
        const currentTimestampSec = Math.floor(Date.now() / 1000);
        if (!token || token.exp < currentTimestampSec + 60) {
            setAuthState({
                user: null,
                initialLoading: false,
            });
            return;
        }
        fetchIdentity(token.token, abortController)
            .then((user) => {
                setAuthState({
                    user,
                    initialLoading: false,
                });
            })
            .catch((e) => {
                if (e.name === "AbortError") {
                    return;
                }
                if (e instanceof APIError) {
                    if (e.api_error_code == "INVALID_TOKEN") {
                        logout(e.message);
                        return;
                    }
                    toast.error(e.message);
                    return;
                }
                toast.error(
                    `An error occurred while trying to fetch your identity: ${e.name}`,
                );
            });
        return () => {
            abortController.abort();
        };
    }, [logout, token]);
    const login = useCallback(
        (token: JWTToken) => {
            setToken(token);
        },
        [setToken],
    );
    const isLoggedIn = useCallback(() => {
        if (authState.initialLoading) {
            return null;
        }
        return !!authState.user;
    }, [authState]);
    return {
        user: authState.user,
        initialLoading: authState.initialLoading,
        tokenStr: authState.user ? token?.token : null,
        logout,
        login,
        isLoggedIn,
    } as AuthContextTools;
}

export function useAuth() {
    const authContext = useContext(AuthContext);
    if (authContext === null) {
        throw new Error("useAuth must be used within a AuthContextProvider");
    }
    return authContext;
}
