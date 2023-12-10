import MainPageHeader from "../components/main/MainPageHeader.tsx";
import DocumentList, { RenderTree } from "../components/main/DocumentList.tsx";
import { createContext, useEffect, useState } from "react";
import Grid from "@mui/material/Grid";
import useMainContext, { MainContextTools } from "../hooks/useMainContext.ts";
import AddDocument from "../components/main/AddDocument.tsx";
import RequirementList from "../components/main/requirement-list/RequirementList.tsx";
import RequirementDetails from "../components/main/RequirementDetails.tsx";
import { fetchDocuments } from "../lib/api/documentService.ts";
import { fetchRequirements } from "../lib/api/requirementService.ts";
import { ReqDocumentWithChildren, Requirement } from "../types.ts";
import AddRequirement from "../components/main/AddRequirement.tsx";

export const MainContext = createContext<MainContextTools | null>(null);

export default function MainPage() {
    const mainContextTools = useMainContext();
    const [mode, setMode] = useState("add");
    const [fetchedDocuments, setFetchedDocuments] = useState<RenderTree>([]);
    const [fetchedPrefixes, setFetchedPrefixes] = useState<string[]>([]);
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

    const updatePrefixes = () => {
        if (fetchedPrefixes.length > 1) {
            const uniqueOptions = Array.from(new Set(fetchedPrefixes)).sort(
                (a, b) => a.localeCompare(b),
            );
            setFetchedPrefixes(uniqueOptions);
        }
    };

    async function getDocuments() {
        // Fetch documents from Django backend
        const data = await fetchDocuments();
        console.log("Fetched documents:", data);
        setFetchedPrefixes([]);
        setFetchedDocuments(data);
        data.forEach(async (document: ReqDocumentWithChildren) => {
            const documentPrefixes = extractPrefixes(document);
            setFetchedPrefixes((prevPrefixes) => [
                ...prevPrefixes,
                ...documentPrefixes,
            ]);
        });
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

    useEffect(() => {
        updatePrefixes();
    }, [fetchedDocuments]);

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
                        flexGrow: 1
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
                            documents={fetchedDocuments}
                            onDeleteDocument={handleDeleteDocument}
                            selectedDocument={selectedDocument}
                            setSelectedDocument={setSelectedDocument}
                            onClickDocument={handleClickDocument}
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
                            overflow: "auto",
                            paddingRight: 4,
                            paddingLeft: 4,
                        }}
                    >
                        <RequirementList
                            requirements={requirements}
                            updateRequirements={handleClickDocument}
                        />
                        {selectedDocument && (
                            <AddRequirement
                                docPrefix={selectedDocument}
                                updateRequirements={handleClickDocument}
                            />
                        )}
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
