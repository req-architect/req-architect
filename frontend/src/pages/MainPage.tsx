import MainPageHeader from "../components/main/MainPageHeader.tsx";
import { createContext, useEffect } from "react";
import useMainContext, { MainContextTools } from "../hooks/useMainContext.ts";
import DocumentEditor from "../components/main/DocumentEditor.tsx";
import useLoginRedirect from "../hooks/useLoginRedirect.ts";
import { useAuth } from "../hooks/useAuthContext.ts";
import { useNavigate } from "react-router-dom";
import useRepoContext from "../hooks/useRepoContext.ts";

/*
    This is the Main Page of the application.
    It provides the user with all the tools in the application regarding the requirements management.
*/

export const MainContext = createContext<MainContextTools | null>(null);

export default function MainPage() {
    const mainContextTools = useMainContext();
    useLoginRedirect(false, "/login");
    const authTools = useAuth();
    const repoContext = useRepoContext();
    const navigate = useNavigate();
    useEffect(() => {
        if (!repoContext.repositoryName) {
            navigate("/repo");
            return;
        }
    }, [navigate, repoContext]);

    return (
        !authTools.initialLoading && (
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
        )
    );
}
