import {useEffect, useState} from 'react';
import {ReqDocument} from "../../types.ts";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Collapse from "@mui/material/Collapse";
import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import IconButton from "@mui/material/IconButton";
import FolderIcon from '@mui/icons-material/Folder';
import DeleteIcon from '@mui/icons-material/Delete';
import ListItem from '@mui/material/ListItem';


const documents = [
    {
        number: 1,
        subdocuments: [1, 2, 3]
    },
    {
        number: 2,
        subdocuments: [1, 2]
    },
    {
        number: 3,
        subdocuments: [1, 2]
    },
    {
        number: 4,
        subdocuments: [1, 2, 3]
    },
    {
        number: 5,
        subdocuments: [1]
    },
    {
        number: 6,
        subdocuments: [1]
    }
];


export default function DocumentList({updateDocument}: {updateDocument: (document: ReqDocument) => void; }) {
    const [openStates, setOpenStates] = useState(Array(documents.length + 1).fill(false));
    useEffect(() => {
        updateDocument({prefix: "Document 1"})
    }, [updateDocument]);
    const handleClick = (index: number) => {
        setOpenStates((prev) =>
            prev.map((value, i) => (i === index ? !value : value))
        );
    };

    const handleDelete = (itemName: string) => {
        const confirmDelete = window.confirm(
            `Are you sure you want to delete ${itemName}?`
        );
        if (confirmDelete) {
            console.log(`Deleted ${itemName}`);
            // Perform deletion logic if needed
        }
    };

    return (
        <List
            sx={{width: '100%', maxWidth: 360, bgcolor: 'background.paper'}}
            component="nav"
        >
        {documents.map((doc) => (
            <>
                <ListItem>
                    <ListItemButton onClick={() => handleClick(doc.number)}>
                        <ListItemIcon>
                            <FolderIcon/>
                        </ListItemIcon>
                        <ListItemText primary= {"Document " + doc.number}/>
                        {openStates[doc.number] ? <ExpandLess/> : <ExpandMore/>}
                    </ListItemButton>
                    <IconButton
                        edge="end"
                        aria-label="delete"
                        onClick={() => handleDelete("Document " + doc.number)}>
                        <DeleteIcon/>
                    </IconButton>
                </ListItem>
                {doc.subdocuments.map((subdoc)=> (
                    <Collapse in={openStates[doc.number]} timeout="auto" unmountOnExit>
                    <List sx={{pl: 2}}>
                        <ListItem>
                            <ListItemButton>
                                <ListItemIcon>
                                    <FolderIcon/>
                                </ListItemIcon>
                                <ListItemText primary={"Document " + doc.number + "." + subdoc}/>
                            </ListItemButton>
                            <IconButton
                                edge="end"
                                aria-label="delete"
                                onClick={() => handleDelete("Document " + doc.number + "." + subdoc)}>
                                <DeleteIcon/>
                            </IconButton>
                        </ListItem>
                    </List>
                </Collapse>
                ))}
            </>
        ))}
        </List>
    );
}
