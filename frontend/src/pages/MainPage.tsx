import MainPageHeader from "../components/main/MainPageHeader.tsx";
import { createContext } from "react";
import useMainContext, { MainContextTools } from "../hooks/useMainContext.ts";
import DocumentEditor from "../components/main/DocumentEditor.tsx";
import useLoginRedirect from "../hooks/useLoginRedirect.ts";
import { useAuth } from "../hooks/useAuthContext.ts";

/*
    This is the Main Page of the application.
    It provides the user with all the tools in the application regarding the requirements management.
*/

export const MainContext = createContext<MainContextTools | null>(null);

export default function MainPage() {
    const mainContextTools = useMainContext();
    useLoginRedirect(false, "/login");
    const authTools = useAuth();
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
