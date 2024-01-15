import { useLocalStorage } from "usehooks-ts";
import { AppUser, JWTToken } from "../types.ts";
import { useCallback, useContext, useEffect, useState } from "react";
import { fetchIdentity } from "../lib/api/authService.ts";
import { AuthContext } from "../App.tsx";

export type AuthContextTools = {
    user: AppUser | null;
    refreshUser: () => void;
};

export default function useAuthContext() {
    const [token] = useLocalStorage<JWTToken>("jwtToken", null);
    const [user, setUser] = useState<AppUser | null>(null);
    const refreshUser = useCallback(() => {
        const currentTimestampSec = Math.floor(Date.now() / 1000);
        if (!token || token.exp < currentTimestampSec + 60) {
            setUser(null);
            return;
        }
        fetchIdentity()
            .then(setUser)
            .catch(() => setUser(null));
    }, [token, setUser]);
    useEffect(() => {
        refreshUser();
    }, [refreshUser]);
    return { user, refreshUser } as AuthContextTools;
}

export function useAuth() {
    const authContext = useContext(AuthContext);
    if (authContext === null) {
        throw new Error("useAuth must be used within a AuthContextProvider");
    }
    return authContext;
}
