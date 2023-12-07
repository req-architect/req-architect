import { Box } from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import { TreeView } from "@mui/x-tree-view/TreeView";
import { TreeItem } from "@mui/x-tree-view/TreeItem";
import DeleteIcon from "@mui/icons-material/Delete";
import IconButton from "@mui/material/IconButton";
import { ReqDocument, ReqDocumentWithChildren } from "../../types.ts";

const isReqDocumentWithChildren = (
    node: ReqDocumentWithChildren | ReqDocument,
): node is ReqDocumentWithChildren => "children" in node;
type RenderTree = (ReqDocument | ReqDocumentWithChildren)[];

const data: RenderTree = [
    {
        prefix: "root",
        children: [
            { prefix: "1" },
            {
                prefix: "2",
                children: [
                    { prefix: "2.1" },
                    {
                        prefix: "2.2",
                        children: [{ prefix: "2.2.1" }],
                    },
                ],
            },
            {
                prefix: "3",
                children: [{ prefix: "3.1" }],
            },
        ],
    },
];

export default function DocumentList() {
    const handleDelete = (event: React.MouseEvent, itemName: string) => {
        event.stopPropagation();
        const confirmDelete = window.confirm(
            `Are you sure you want to delete ${itemName}?`,
        );
        if (confirmDelete) {
            console.log(`Deleted ${itemName}`);
            // Perform deletion logic if needed
        }
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
                        <div>
                            Document: {node.prefix}
                            {isReqDocumentWithChildren(node) &&
                                node.children && (
                                    <IconButton
                                        edge="end"
                                        aria-label="delete"
                                        onClick={(event) =>
                                            handleDelete(event, node.prefix)
                                        }
                                    >
                                        <DeleteIcon sx={IconButtonStyles} />
                                    </IconButton>
                                )}
                        </div>
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
                {renderTree(data)}
            </TreeView>
        </Box>
    );
}
