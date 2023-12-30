import MainPageHeader from "../components/main/MainPageHeader.tsx";
import DocumentList from "../components/main/DocumentList.tsx";
import { createContext, useEffect, useState } from "react";
import Grid from "@mui/material/Grid";
import useMainContext, { MainContextTools } from "../hooks/useMainContext.ts";
import AddDocument, { Mode } from "../components/main/AddDocument.tsx";
import RequirementList from "../components/main/requirement-list/RequirementList.tsx";
import RequirementDetails from "../components/main/RequirementDetails.tsx";
import { fetchDocuments } from "../lib/api/documentService.ts";
import { fetchRequirements } from "../lib/api/requirementService.ts";
import { ReqDocumentWithChildren, Requirement } from "../types.ts";
import AddRequirement from "../components/main/AddRequirement.tsx";
import { Box } from "@mui/material";

export const MainContext = createContext<MainContextTools | null>(null);

export default function MainPage() {
    const mainContextTools = useMainContext();
    const [mode, setMode] = useState<Mode>("add");
    const [fetchedRootDocument, setFetchedRootDocument] =
        useState<ReqDocumentWithChildren | null>(null);
    const [selectedDocument, setSelectedDocument] = useState<string>("");
    const [requirements, setRequirements] = useState<Requirement[]>([]);

    const extractPrefixes = (document: ReqDocumentWithChildren) => {
        let prefixes: string[] = [document.prefix];

        if (document.children && document.children.length > 0) {
            document.children.forEach((child) => {
                prefixes = [...prefixes, ...extractPrefixes(child)];
            });
        }
        return prefixes;
    };

    const fetchedPrefixes = fetchedRootDocument
        ? extractPrefixes(fetchedRootDocument)
        : [];

    async function getDocuments() {
        // Fetch documents from Django backend
        const data = await fetchDocuments();
        console.log("Fetched documents:", data);
        if (data.length > 0) {
            setFetchedRootDocument(data[0]);
        } else {
            setFetchedRootDocument(null);
        }
    }

    async function getRequirements(docPrefix: string) {
        // Fetch requirements from Django backend
        if (docPrefix === "") {
            console.log("No document selected");
            return;
        } else {
            const data = await fetchRequirements(docPrefix);
            console.log("Fetched requirements:", data);
            setRequirements(data);
        }
        mainContextTools?.updateSelectedRequirement(null);
    }

    useEffect(() => {
        Promise.all([getDocuments(), getRequirements(selectedDocument)]);
    }, [selectedDocument]);

    const handleDeleteDocument = async () => {
        await getDocuments();
    };

    const handleAddDocument = async () => {
        await getDocuments();
    };

    const handleClickDocument = async () => {
        await getRequirements(selectedDocument);
    };

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
                <Grid
                    container
                    justifyContent={"space-between"}
                    sx={{
                        borderBottom: "0.5px solid green",
                        overflow: "hidden",
                        flexGrow: 1,
                    }}
                >
                    <Grid
                        item
                        xs={2}
                        display={"flex"}
                        flexDirection={"column"}
                        borderRight={"1px solid green"}
                    >
                        <DocumentList
                            rootDocument={fetchedRootDocument}
                            refreshDocuments={handleDeleteDocument}
                            setSelectedDocument={setSelectedDocument}
                        />
                        <AddDocument
                            mode={mode}
                            setMode={setMode}
                            prefixes={fetchedPrefixes}
                            onAddDocument={handleAddDocument}
                        />
                    </Grid>
                    <Grid
                        item
                        xs={8}
                        sx={{
                            height: "100%",
                        }}
                    >
                        <Box sx={{ height: "100%", overflowY: "auto" }}>
                            <RequirementList
                                requirements={requirements}
                                updateRequirements={handleClickDocument}
                            />
                        </Box>
                        <Box
                            sx={{
                                height: "0%",
                                display: "flex",
                                justifyContent: "flex-end",
                                alignItems: "flex-end",
                            }}
                        >
                            <AddRequirement
                                docPrefix={selectedDocument}
                                updateRequirements={handleClickDocument}
                            />
                        </Box>
                    </Grid>
                    {/* <Grid item xs={1} /> */}
                    <Grid item xs={2}>
                        <RequirementDetails />
                    </Grid>
                </Grid>
            </div>
        </MainContext.Provider>
    );
}
