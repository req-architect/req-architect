import Grid from "@mui/material/Grid";
import DocumentList from "./DocumentList.tsx";
import AddDocument from "./AddDocument.tsx";
import { useEffect, useState } from "react";
import { ReqDocumentWithChildren } from "../../types.ts";
import { fetchDocuments } from "../../lib/api/documentService.ts";
import RequirementsEditor from "./RequirementsEditor.tsx";

export default function DocumentEditor() {
    const [fetchedRootDocument, setFetchedRootDocument] =
        useState<ReqDocumentWithChildren | null>(null);
    async function refreshDocuments() {
        const data = await fetchDocuments();
        console.log("Fetched documents:", data);
        if (data.length > 0) {
            setFetchedRootDocument(data[0]);
        } else {
            setFetchedRootDocument(null);
        }
    }
    useEffect(() => {
        refreshDocuments();
    }, []);
    return (
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
                    refreshDocuments={refreshDocuments}
                />
                <AddDocument
                    rootDocument={fetchedRootDocument}
                    refreshDocuments={refreshDocuments}
                />
            </Grid>
            <RequirementsEditor />
        </Grid>
    );
}
