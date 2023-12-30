import { Box, Typography } from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import { TreeView } from "@mui/x-tree-view/TreeView";
import { TreeItem } from "@mui/x-tree-view/TreeItem";
import DeleteIcon from "@mui/icons-material/Delete";
import IconButton from "@mui/material/IconButton";
import FolderIcon from "@mui/icons-material/Folder";
import { ReqDocument, ReqDocumentWithChildren } from "../../types.ts";
import { deleteDocument } from "../../lib/api/documentService.ts";
import { useEffect } from "react";
import { IconButtonStyles } from "../../lib/styles.ts";

export default function DocumentList({
    rootDocument,
    onDeleteDocument,
    selectedDocument,
    setSelectedDocument,
    onClickDocument,
}: {
    rootDocument: ReqDocumentWithChildren | null;
    onDeleteDocument: () => void;
    selectedDocument: string;
    setSelectedDocument: (selectedDocument: string) => void;
    onClickDocument: () => void;
}) {
    const handleDelete = async (event: React.MouseEvent, itemName: string) => {
        event.stopPropagation();
        const confirmDelete = window.confirm(
            `Are you sure you want to delete ${itemName}?`,
        );
        if (confirmDelete) {
            console.log(`Deleted ${itemName}`);
            await deleteDocument(itemName);
        }
        onDeleteDocument();
    };

    const renderTree = (nodes: ReqDocumentWithChildren[]) => (
        <>
            {nodes.map((node) => (
                <div
                    key={node.prefix}
                    onClick={(event) => handleTreeItemClick(event, node)}
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

    const handleTreeItemClick = (
        event: React.MouseEvent,
        node: ReqDocumentWithChildren | ReqDocument,
    ) => {
        event.stopPropagation();
        setSelectedDocument(node.prefix);
    };

    useEffect(() => {
        console.log("Selected document:", selectedDocument);
        onClickDocument();
    }, [selectedDocument]);

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
