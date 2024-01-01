import MainPageHeader from "../components/main/MainPageHeader.tsx";
import { createContext } from "react";
import useMainContext, { MainContextTools } from "../hooks/useMainContext.ts";
import DocumentEditor from "../components/main/DocumentEditor.tsx";

export const MainContext = createContext<MainContextTools | null>(null);

export default function MainPage() {
    const mainContextTools = useMainContext();
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
