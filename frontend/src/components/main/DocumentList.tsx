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


const documents = [1, 2, 3, 4, 5, 6, 7, 8, 9];


export default function DocumentList({updateDocument}: {updateDocument: (document: ReqDocument) => void; }) {
    const [openStates, setOpenStates] = useState(Array(documents.length).fill(false));
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
            {documents.map((doc_nr) => (
                <ListItem>
                <ListItemButton onClick={() => handleClick(doc_nr)}>
                    <ListItemIcon>
                        <FolderIcon/>
                    </ListItemIcon>
                    <ListItemText primary= {"Document " + doc_nr}/>
                    {openStates[doc_nr] ? <ExpandLess/> : <ExpandMore/>}
                </ListItemButton>
                <IconButton
                    edge="end"
                    aria-label="delete"
                    onClick={() => handleDelete("Document " + doc_nr)}>
                    <DeleteIcon/>
                </IconButton>
            </ListItem>
            ))}
        </List>
    );
}

{/* <ListItem>
                <ListItemButton onClick={() => handleClick(0)}>
                    <ListItemIcon>
                        <FolderIcon/>
                    </ListItemIcon>
                    <ListItemText primary="Document 1"/>
                    {openStates[0] ? <ExpandLess/> : <ExpandMore/>}
                </ListItemButton>
                <IconButton
                    edge="end"
                    aria-label="delete"
                    onClick={() => handleDelete("Document 1")}>
                    <DeleteIcon/>
                </IconButton>
            </ListItem>
            <Collapse in={openStates[0]} timeout="auto" unmountOnExit>
                <List sx={{pl: 2}}>
                    <ListItem>
                        <ListItemButton>
                            <ListItemIcon>
                                <FolderIcon/>
                            </ListItemIcon>
                            <ListItemText primary="Document 1.1"/>
                        </ListItemButton>
                        <IconButton
                            edge="end"
                            aria-label="delete"
                            onClick={() => handleDelete("Document 1.1")}>
                            <DeleteIcon/>
                        </IconButton>
                    </ListItem>
                </List>
            </Collapse>
            <ListItem>
                <ListItemButton onClick={() => handleClick(1)}>
                    <ListItemIcon>
                        <FolderIcon/>
                    </ListItemIcon>
                    <ListItemText primary="Document 2"/>
                    {openStates[1] ? <ExpandLess/> : <ExpandMore/>}
                </ListItemButton>
                <IconButton
                    edge="end"
                    aria-label="delete"
                    onClick={() => handleDelete("Document 2")}>
                    <DeleteIcon/>
                </IconButton>
            </ListItem>
            <Collapse in={openStates[1]} timeout="auto" unmountOnExit>
                <List sx={{pl: 2}}>
                    <ListItem>
                        <ListItemButton>
                            <ListItemIcon>
                                <FolderIcon/>
                            </ListItemIcon>
                            <ListItemText primary="Document 2.1"/>
                        </ListItemButton>
                        <IconButton
                            edge="end"
                            aria-label="delete"
                            onClick={() => handleDelete("Document 2.1")}>
                            <DeleteIcon/>
                        </IconButton>
                    </ListItem>
                    <ListItem>
                        <ListItemButton>
                            <ListItemIcon>
                                <FolderIcon/>
                            </ListItemIcon>
                            <ListItemText primary="Document 2.2"/>
                        </ListItemButton>
                        <IconButton
                            edge="end"
                            aria-label="delete"
                            onClick={() => handleDelete("Document 2.2")}>
                            <DeleteIcon/>
                        </IconButton>
                    </ListItem>
                </List>
            </Collapse> */}