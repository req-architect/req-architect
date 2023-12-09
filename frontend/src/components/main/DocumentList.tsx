import { Box } from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import { TreeView } from "@mui/x-tree-view/TreeView";
import { TreeItem } from "@mui/x-tree-view/TreeItem";
import DeleteIcon from "@mui/icons-material/Delete";
import IconButton from "@mui/material/IconButton";
import FolderIcon from '@mui/icons-material/Folder';
import { ReqDocument, ReqDocumentWithChildren } from "../../types.ts";
import { DeleteDocument } from "../../hooks/MainFunctions.ts";

const isReqDocumentWithChildren = (
    node: ReqDocumentWithChildren | ReqDocument,
): node is ReqDocumentWithChildren => "children" in node;
export type RenderTree = (ReqDocument | ReqDocumentWithChildren)[];

export default function DocumentList({ documents, onDeleteDocument }: {documents: RenderTree; onDeleteDocument: () => void;}) {
    
    const handleDelete = async (event: React.MouseEvent, itemName: string) => {
        event.stopPropagation();
        const confirmDelete = window.confirm(
            `Are you sure you want to delete ${itemName}?`,
        );
        if (confirmDelete) {
            console.log(`Deleted ${itemName}`);
            await DeleteDocument(itemName);
        }
        onDeleteDocument();
    };

    const IconButtonStyles = {
        color: "#666666",
        "&:hover": {
            color: "darkred",
        },
    };
    

    const renderTree = (nodes: ReqDocumentWithChildren[] | ReqDocument[]) => (
        <>
            {nodes.map((node) => (
                <TreeItem
                    key={node.prefix}
                    nodeId={node.prefix}
                    label={
                        <Box sx={{display: "flex", alignItems: "center"}}>
                            <FolderIcon sx={{color: IconButtonStyles.color}}/>
                            Document: {node.prefix}
                            {/* {isReqDocumentWithChildren(node) &&
                                node.children && ( */}
                                    <IconButton
                                        edge="end"
                                        aria-label="delete"
                                        onClick={(event) =>
                                            handleDelete(event, node.prefix)
                                        }
                                    >
                                        <DeleteIcon sx={IconButtonStyles} />
                                    </IconButton>
                                {/* )} */}
                        </Box>
                    }
                >
                    {isReqDocumentWithChildren(node) &&
                        node.children &&
                        renderTree(node.children)}
                </TreeItem>
            ))}
        </>
    );

    return (
        <Box
            sx={{
                minHeight: 180,
                flexGrow: 1,
                maxWidth: 300,
                overflowY: "auto",
            }}
        >
            <TreeView
                defaultCollapseIcon={<ExpandMoreIcon />}
                defaultExpandIcon={<ChevronRightIcon />}
            >
                {renderTree(documents)}
            </TreeView>
        </Box>
    );
}

