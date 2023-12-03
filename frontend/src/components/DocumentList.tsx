import * as React from 'react';
import { ReqDocument } from "../types.ts";
import { useEffect, useState } from "react";
import ListSubheader from "@mui/material/ListSubheader";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Collapse from "@mui/material/Collapse";
import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import DescriptionIcon from "@mui/icons-material/Description";
import IconButton from "@mui/material/IconButton";
import Grid from "@mui/material/Grid";
import FolderIcon from '@mui/icons-material/Folder';
import DeleteIcon from '@mui/icons-material/Delete';
import SendIcon from '@mui/icons-material/Send';
import StarBorder from '@mui/icons-material/StarBorder';
import ListItem from '@mui/material/ListItem';
import Button from '@mui/material/Button';

export default function DocumentList({
  updateDocument,
}: {
  updateDocument: (document: ReqDocument) => void;
}) {
  const [text, setText] = useState("");
  useEffect(() => {
    // fetch(import.meta.env.VITE_APP_API_URL + '/demoapp/hello').then(res => res.text()).then(setText)
    setText("TEST");
  }, []);

  const [openStates, setOpenStates] = useState([false, false]);

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
      alert(`Deleted ${itemName}`);
      // Perform deletion logic if needed
    }
  };


  return (
    <List
      sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}
      component="nav"
    >
      <ListItem>
        <ListItemButton onClick={() => handleClick(0)}>
          <ListItemIcon>
            <FolderIcon />
          </ListItemIcon>
          <ListItemText primary="Document 1" />
          {openStates[0] ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <IconButton
          edge="end"
          aria-label="delete"
          onClick={() => handleDelete("Document 1")}>
          <DeleteIcon/>
        </IconButton>
      </ListItem>
      <Collapse in={openStates[0]} timeout="auto" unmountOnExit>
        <List sx={{ pl: 2 }}>
          <ListItem>
            <ListItemButton>
              <ListItemIcon>
                <FolderIcon />
              </ListItemIcon>
              <ListItemText primary="Document 1.1" />
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
            <FolderIcon />
          </ListItemIcon>
          <ListItemText primary="Document 2" />
          {openStates[0] ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <IconButton
          edge="end"
          aria-label="delete"
          onClick={() => handleDelete("Document 2")}>
          <DeleteIcon/>
        </IconButton>
      </ListItem>
      <Collapse in={openStates[1]} timeout="auto" unmountOnExit>
        <List sx={{ pl: 2 }}>
          <ListItem>
            <ListItemButton>
              <ListItemIcon>
                <FolderIcon />
              </ListItemIcon>
              <ListItemText primary="Document 2.1" />
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
                <FolderIcon />
              </ListItemIcon>
              <ListItemText primary="Document 2.2" />
            </ListItemButton>
            <IconButton
                edge="end"
                aria-label="delete"
                onClick={() => handleDelete("Document 2.2")}>
                <DeleteIcon/>
              </IconButton>
          </ListItem>
        </List>
      </Collapse>
    </List>
  );
}

{/* <Grid
      sx={{
        height: "90%",
      }}
    >
      <List
        sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}
        component="nav"
        aria-labelledby="nested-list-subheader"
        subheader={
          <ListSubheader component="div" id="nested-list-subheader">
            Dokumenty
          </ListSubheader>
        }
      >
        <ListItemButton onClick={() => handleIsOpen(0)}>
          <ListItemIcon>
            <DescriptionIcon color="disabled" />
          </ListItemIcon>
          <ListItemText primary="Document 1" />
          {openStates[0] ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={openStates[0]} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <ListItemButton sx={{ pl: 4 }}>
              <ListItemIcon>
                <DescriptionIcon color="disabled" />
              </ListItemIcon>
              <ListItemText primary="Document 1.2" />
              <IconButton
                edge="end"
                aria-label="delete"
                onClick={() => handleDelete("Document 1.2")}
              >
                <DeleteIcon color="error" />
              </IconButton>
            </ListItemButton>
            <ListItemButton sx={{ pl: 4 }}>
              <ListItemIcon>
                <DescriptionIcon color="disabled" />
              </ListItemIcon>
              <ListItemText primary="Document 1.3" />
              <IconButton
                edge="end"
                aria-label="delete"
                onClick={() => handleDelete("Document 1.3")}
              >
                <DeleteIcon color="error" />
              </IconButton>
            </ListItemButton>
          </List>
        </Collapse>
        <ListItemButton onClick={() => handleIsOpen(1)}>
          <ListItemIcon>
            <DescriptionIcon color="disabled" />
          </ListItemIcon>
          <ListItemText primary={text} />
          {openStates[1] ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={openStates[1]} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <ListItemButton sx={{ pl: 4 }}>
              <ListItemIcon>
                <DescriptionIcon color="disabled" />
              </ListItemIcon>
              <ListItemText primary="Document 2.2" />
              <IconButton
                edge="end"
                aria-label="delete"
                onClick={() => handleDelete("Document 2.2")}
              >
                <DeleteIcon color="error" />
              </IconButton>
            </ListItemButton>
          </List>
        </Collapse>
      </List>
    </Grid> */}