import React, { useContext, useState } from "react";
import { Requirement } from "../../../types.ts";
import { IconButton, TextField, Typography, Box, Grid } from "@mui/material";
import RenderedRequirementText from "./RenderedRequirementText.tsx";
import UndoIcon from "@mui/icons-material/Undo";
import DoneIcon from "@mui/icons-material/Done";
import DeleteIcon from "@mui/icons-material/Delete";
import { MainContext } from "../../../pages/MainPage.tsx";
import { IconButtonStyles } from "../../../lib/styles.ts";
import {
    deleteRequirement,
    putRequirement,
} from "../../../lib/api/requirementService.ts";

export default function RequirementEditMode({
    requirement,
    updateRequirements,
}: {
    requirement: Requirement;
    updateRequirements: () => void;
}) {
    const [editedText, setEditedText] = useState(requirement.text);
    const contextTools = useContext(MainContext);
    function handleAbort() {
        if (editedText !== requirement.text) {
            // confirm abort
            if (!window.confirm("Are you sure you want to abort?")) {
                return;
            }
        }
        contextTools?.updateEditMode(false);
        contextTools?.updateSelectedRequirement(null);
    }
    async function handleSave() {
        // TODO: update requirement in database and reload
        contextTools?.updateEditMode(false);
        contextTools?.updateSelectedRequirement(null);
        await putRequirement(requirement.id, editedText);
        updateRequirements();
    }
    async function handleDelete() {
        contextTools?.updateEditMode(false);
        contextTools?.updateSelectedRequirement(null);
        await deleteRequirement(requirement.id);
        updateRequirements();
    }
    return (
        <Grid container>
            <Grid item xs={6} sx={{borderRight: "1px solid green"}}>
                    <Typography variant="h6" color="black" sx={{ml: 1, mt: 1}}>
                        Req {requirement.id}
                    </Typography>
                <Box sx={{m: 4}}>
                    <TextField
                    multiline
                    rows={12}
                    value={editedText}
                    onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                        setEditedText(event.target.value);
                    }}
                    sx={{ width: "100%"}}
                    />
                </Box>
            </Grid>
            <Grid item xs={6}>
                <Box sx={{display: "flex", justifyContent: "end"}}>
                    <IconButton aria-label="save" color="success" onClick={handleSave}>
                        <DoneIcon />
                    </IconButton>
                    <IconButton aria-label="abort" color="error" onClick={handleAbort}>
                        <UndoIcon />
                    </IconButton>
                    <IconButton aria-label="delete" onClick={handleDelete}>
                        <DeleteIcon sx={IconButtonStyles} />
                    </IconButton>
                </Box>
                <Box sx={{m: 4}}>
                    <RenderedRequirementText text={editedText} />
                </Box>
            </Grid>
        </Grid>
    );
}
