import MainPageHeader from "../components/main/MainPageHeader.tsx";
import DocumentList from "../components/main/DocumentList.tsx";
import { createContext, useState } from "react";
import Grid from "@mui/material/Grid";
import { Container } from "@mui/material";
import useMainContext, { MainContextTools } from "../hooks/useMainContext.ts";
import AddDocument from "../components/main/AddDocument.tsx";
import RequirementList from "../components/main/requirement-list/RequirementList.tsx";
import RequirementDetails from "../components/main/RequirementDetails.tsx";

export const MainContext = createContext<MainContextTools | null>(null);

export default function MainPage() {
    const mainContextTools = useMainContext();
    const [mode, setMode] = useState("add");

    return (
        <MainContext.Provider value={mainContextTools}>
            <div
                style={{
                    width: "100%",
                    minWidth: 1025,
                    height: "100vh",
                    minHeight: 700,
                    display: "flex",
                    flexDirection: "column",
                }}
            >
                <MainPageHeader />
                <Grid
                    container
                    justifyContent={"space-between"}
                    sx={{
                        borderBottom: "0.5px solid green",
                        overflow: "hidden",
                        height: "95vh",
                    }}
                >
                    <Grid item xs={3} display={"flex"} flexDirection={"column"} borderRight={"1px solid green"}>
                        <Container
                            sx={{
                                maxHeight: mode === "add" ? "74vh" : "53vh",
                                overflowY: "auto",
                            }}
                        >
                            <DocumentList />
                        </Container>
                        <AddDocument mode={mode} setMode={setMode} />
                    </Grid>
                    <Grid item xs={6} sx={{ height: "100%", overflow: "auto" }}>
                        <RequirementList />
                    </Grid>
                    <Grid item xs={0} />
                    <Grid item xs={2}>
                        <RequirementDetails />
                    </Grid>
                </Grid>
            </div>
        </MainContext.Provider>
    );
}
