import Grid from "@mui/material/Grid";
import DocumentList from "./DocumentList.tsx";
import AddDocument from "./AddDocument.tsx";
import { useCallback, useEffect, useState } from "react";
import { ReqDocumentWithChildren } from "../../types.ts";
import { fetchDocuments } from "../../lib/api/documentService.ts";
import RequirementsEditor from "./RequirementsEditor.tsx";
import { useMainContextTools } from "../../hooks/useMainContext.ts";

function isInTree(root: ReqDocumentWithChildren, prefix: string): boolean {
    if (root.prefix === prefix) {
        return true;
    }
    if (!root.children || root.children.length === 0) {
        return false;
    }
    for (const child of root.children) {
        if (isInTree(child, prefix)) {
            return true;
        }
    }
    return false;
}

export default function DocumentEditor() {
    const mainContextTools = useMainContextTools();
    const [fetchedRootDocument, setFetchedRootDocument] =
        useState<ReqDocumentWithChildren | null>(null);

    const refreshDocuments = useCallback(async () => {
        const data = await fetchDocuments();
        if (data.length > 0) {
            setFetchedRootDocument(data[0]);
        } else {
            setFetchedRootDocument(null);
        }
    }, []);

    useEffect(() => {
        refreshDocuments().then();
    }, [refreshDocuments]);

    useEffect(() => {
        if (mainContextTools.data.selectedDocumentPrefix) {
            if (
                fetchedRootDocument &&
                !isInTree(
                    fetchedRootDocument,
                    mainContextTools.data.selectedDocumentPrefix,
                )
            ) {
                mainContextTools.updateSelectedDocument(null);
            }
            if (!fetchedRootDocument) {
                mainContextTools.updateSelectedDocument(null);
            }
        }
    }, [mainContextTools, fetchedRootDocument]);

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
