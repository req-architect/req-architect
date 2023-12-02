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
import DeleteIcon from "@mui/icons-material/Delete";
import IconButton from "@mui/material/IconButton";
import Grid from "@mui/material/Grid";

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

  const handleIsOpen = (index: number) => {
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
    <Grid
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
    </Grid>
  );
}
