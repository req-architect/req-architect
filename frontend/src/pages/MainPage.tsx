import MainPageHeader from "../components/main/MainPageHeader.tsx";
import DocumentList from "../components/main/DocumentList.tsx";
import RequirementList from "../components/main/RequirementList.tsx";
import RequirementDetails from "../components/main/RequirementDetails.tsx";
import { useState } from "react";
import { ReqDocument, Requirement } from "../types.ts";
import Grid from "@mui/material/Grid";
import AddDocument from "../components/main/AddDocument.tsx";
import Metadata from "../components/main/Metadata.tsx";
import { Container } from "@mui/material";

export default function MainPage() {
    const [selectedDocReq, setSelectedDocReq] = useState<
        [ReqDocument | null, Requirement | null]
    >([null, null]);

    const [mode, setMode] = useState("add");

    function updateDocument(document: ReqDocument) {
        setSelectedDocReq([document, null]);
    }

    function updateRequirement(requirement: Requirement) {
        setSelectedDocReq((prev) => [prev[0], requirement]);
    }

    function addDocument(document: ReqDocument) {
        setSelectedDocReq([document, null]);
    }

    return (
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
                    minHeight: "30vh",
                }}
            >
                <Grid item xs={3} display={"flex"} flexDirection={"column"}>
                    <Container
                        sx={{
                            maxHeight: mode === "add" ? "74vh" : "53vh",
                            overflowY: "auto",
                        }}
                    >
                        <DocumentList updateDocument={updateDocument} />
                    </Container>
                    <AddDocument
                        addDocument={addDocument}
                        mode={mode}
                        setMode={setMode}
                    />
                </Grid>
                <Grid item xs={6} sx={{ height: "100%", overflow: "auto" }}>
                    <RequirementList />
                </Grid>
                <Grid item xs={0} />
                <Grid item xs={2}>
                    <Metadata />
                </Grid>
            </Grid>
        </div>
    );
}
