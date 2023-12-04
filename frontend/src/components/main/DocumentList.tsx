import { ReqDocument } from "../../types.ts";
import Box from "@mui/material/Box";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import { TreeView } from "@mui/x-tree-view/TreeView";
import { TreeItem } from "@mui/x-tree-view/TreeItem";
import DeleteIcon from "@mui/icons-material/Delete";
import IconButton from "@mui/material/IconButton";

interface RenderTree {
    id: string;
    name: string;
    children?: readonly RenderTree[];
}

const data: RenderTree = {
    id: "root",
    name: "Documents",
    children: [
        {
            id: "1",
            name: "Document 1",
        },
        {
            id: "2",
            name: "Document 2",
            children: [
                {
                    id: "2.1",
                    name: "Document 2.1",
                },
                {
                    id: "2.2",
                    name: "Document 2.2",
                    children: [
                        {
                            id: "2.2.1",
                            name: "Document 2.2.1",
                        },
                    ],
                },
            ],
        },
        {
            id: "3",
            name: "Document 3",
            children: [
                {
                    id: "3.1",
                    name: "Document 3.1",
                },
            ],
        },
    ],
};

export default function DocumentList({
    updateDocument,
}: {
    updateDocument: (document: ReqDocument) => void;
}) {
    const handleDelete = (event: React.MouseEvent, itemName: string) => {
        event.stopPropagation();
        const confirmDelete = window.confirm(
            `Are you sure you want to delete ${itemName}?`
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

    const renderTree = (nodes: RenderTree) => (
        <TreeItem
            key={nodes.id}
            nodeId={nodes.id}
            label={
                <div>
                    {nodes.name}
                    <IconButton
                        edge="end"
                        aria-label="delete"
                        onClick={(event) => handleDelete(event, nodes.name)}
                    >
                        <DeleteIcon sx={IconButtonStyles} />
                    </IconButton>
                </div>
            }
        >
            {Array.isArray(nodes.children)
                ? nodes.children.map((node) => renderTree(node))
                : null}
        </TreeItem>
    );

    return (
        <Box sx={{ minHeight: 180, flexGrow: 1, maxWidth: 300 }}>
            <TreeView
                defaultCollapseIcon={<ExpandMoreIcon />}
                defaultExpandIcon={<ChevronRightIcon />}
            >
                {renderTree(data)}
            </TreeView>
        </Box>
    );
}
