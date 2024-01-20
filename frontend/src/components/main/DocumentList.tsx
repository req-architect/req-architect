import { Box, Typography } from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import { TreeView } from "@mui/x-tree-view/TreeView";
import { TreeItem } from "@mui/x-tree-view/TreeItem";
import DeleteIcon from "@mui/icons-material/Delete";
import IconButton from "@mui/material/IconButton";
import FolderIcon from "@mui/icons-material/Folder";
import { ReqDocumentWithChildren } from "../../types.ts";
import { deleteDocument } from "../../lib/api/documentService.ts";
import { IconButtonStyles } from "../../lib/styles.ts";
import { useMainContextTools } from "../../hooks/useMainContext.ts";
import React from "react";
import { defaultConfirm } from "../../lib/defaultConfirm.ts";
import { useAuth } from "../../hooks/useAuthContext.ts";
import useRepoContext from "../../hooks/useRepoContext.ts";

/* 
    This component is used to display the document list.
    It will display the document tree and allow the user to delete documents.
*/

export default function DocumentList({
    rootDocument,
    refreshDocuments,
}: {
    rootDocument: ReqDocumentWithChildren | null;
    refreshDocuments: () => void;
}) {
    const mainContextTools = useMainContextTools();
    const authTools = useAuth();
    const repoTools = useRepoContext();
    const handleDelete = async (event: React.MouseEvent, itemName: string) => {
        event.stopPropagation();
        if (!authTools.tokenStr || !repoTools.repositoryName) {
            return;
        }
        defaultConfirm(
            "Delete confirmation",
            `Are you sure you want to delete ${itemName}?`,
            async () => {
                if (!authTools.tokenStr || !repoTools.repositoryName) {
                    return;
                }
                await deleteDocument(
                    authTools.tokenStr,
                    repoTools.repositoryName,
                    itemName,
                );
                refreshDocuments();
            },
        );
    };

    const renderTree = (nodes: ReqDocumentWithChildren[]) => (
        <>
            {nodes.map((node) => (
                <div
                    key={node.prefix}
                    onClick={(event) => {
                        event.stopPropagation();
                        mainContextTools.updateSelectedDocument(node.prefix);
                    }}
                >
                    <TreeItem
                        nodeId={node.prefix}
                        label={
                            <Box sx={{ display: "flex", alignItems: "center" }}>
                                <FolderIcon
                                    sx={{ color: IconButtonStyles.color }}
                                />
                                <Typography
                                    noWrap
                                    sx={{
                                        minWidth: "fit-content",
                                        flexGrow: 1,
                                    }}
                                >
                                    Document: {node.prefix}
                                </Typography>
                                <IconButton
                                    edge="end"
                                    aria-label="delete"
                                    onClick={(event) =>
                                        handleDelete(event, node.prefix)
                                    }
                                >
                                    <DeleteIcon sx={IconButtonStyles} />
                                </IconButton>
                            </Box>
                        }
                    >
                        {node.children && renderTree(node.children)}
                    </TreeItem>
                </div>
            ))}
        </>
    );

    return (
        <Box
            sx={{
                minHeight: "20vh",
                flexGrow: 1,
                maxWidth: 300,
                height: "55vh",
                overflowY: "auto",
            }}
        >
            <TreeView
                defaultCollapseIcon={<ExpandMoreIcon />}
                defaultExpandIcon={<ChevronRightIcon />}
                sx={{ minWidth: "fit-content" }}
            >
                {rootDocument && renderTree([rootDocument])}
            </TreeView>
        </Box>
    );
}
