import { useLocalStorage } from "usehooks-ts";
import { AppUser, JWTToken } from "../types.ts";
import { useCallback, useContext, useEffect, useState } from "react";
import { fetchIdentity } from "../lib/api/authService.ts";
import { AuthContext } from "../App.tsx";
import { toast } from "react-toastify";

export type AuthContextTools = {
    tokenStr: string | null;
    user: AppUser | null;
    initialLoading: boolean;
    logout: () => void;
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
                if (!(e.name === "AbortError")) {
                    setAuthState({
                        user: null,
                        initialLoading: false,
                    });
                }
            });
        return () => {
            abortController.abort();
        };
    }, [token]);
    const logout = useCallback(() => {
        setToken(null);
        toast.info("You have been logged out.");
    }, [setToken]);
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
