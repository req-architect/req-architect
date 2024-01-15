import MainPageHeader from "../components/main/MainPageHeader.tsx";
import { createContext, useEffect } from "react";
import useMainContext, { MainContextTools } from "../hooks/useMainContext.ts";
import DocumentEditor from "../components/main/DocumentEditor.tsx";
import { useAuth } from "../hooks/useAuthContext.ts";
import { useNavigate } from "react-router-dom";

export const MainContext = createContext<MainContextTools | null>(null);

export default function MainPage() {
    const mainContextTools = useMainContext();
    const authTools = useAuth();
    const navigate = useNavigate();
    useEffect(() => {
        if (!authTools.user) {
            navigate("/login");
            return;
        }
    }, [navigate, authTools.user]);
    return (
        <MainContext.Provider value={mainContextTools}>
            <div
                style={{
                    width: "100%",
                    minWidth: 1200,
                    height: "100vh",
                    minHeight: 700,
                    display: "flex",
                    flexDirection: "column",
                }}
            >
                <MainPageHeader />
                <DocumentEditor />
            </div>
        </MainContext.Provider>
    );
}
