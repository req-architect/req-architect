import React, { useState } from "react";
import { IconButton, TextField, Typography, Box, Grid } from "@mui/material";
import RenderedRequirementText from "./RenderedRequirementText.tsx";
import UndoIcon from "@mui/icons-material/Undo";
import DoneIcon from "@mui/icons-material/Done";
import DeleteIcon from "@mui/icons-material/Delete";
import { IconButtonStyles } from "../../../lib/styles.ts";
import {
    deleteRequirement,
    putRequirement,
} from "../../../lib/api/requirementService.ts";
import { useMainContextTools } from "../../../hooks/useMainContext.ts";
import useRequirementContext from "../../../hooks/useRequirementContext.ts";
import { defaultConfirm } from "../../../lib/defaultConfirm.ts";

export default function RequirementEditMode() {
    const { requirement, refreshRequirements } = useRequirementContext();
    const [editedText, setEditedText] = useState(requirement.text);
    const contextTools = useMainContextTools();
    function handleAbort() {
        if (editedText !== requirement.text) {
            // confirm abort
            defaultConfirm(
                "Abort confirmation",
                "Are you sure you want to abort your changes?",
                () => {
                    contextTools.updateSelectedRequirement(null);
                },
            );
        } else {
            contextTools.updateSelectedRequirement(null);
        }
    }
    async function handleSave() {
        contextTools.updateSelectedRequirement(null);
        await putRequirement(requirement.id, editedText);
        refreshRequirements();
    }
    async function handleDelete() {
        contextTools.updateSelectedRequirement(null);
        await deleteRequirement(requirement.id);
        refreshRequirements();
    }
    return (
        <Grid container>
            <Grid item xs={6} sx={{ borderRight: "1px solid green" }}>
                <Typography
                    variant="h6"
                    color="black"
                    fontWeight={"bold"}
                    sx={{ ml: 1, mt: 1 }}
                >
                    Req {requirement.id}
                </Typography>
                <Box sx={{ m: 4 }}>
                    <TextField
                        multiline
                        rows={12}
                        value={editedText}
                        onChange={(
                            event: React.ChangeEvent<HTMLInputElement>,
                        ) => {
                            setEditedText(event.target.value);
                        }}
                        sx={{ width: "100%" }}
                    />
                </Box>
            </Grid>
            <Grid item xs={6}>
                <Box sx={{ display: "flex", justifyContent: "end" }}>
                    <IconButton
                        aria-label="save"
                        color="success"
                        onClick={handleSave}
                    >
                        <DoneIcon />
                    </IconButton>
                    <IconButton
                        aria-label="abort"
                        color="error"
                        onClick={handleAbort}
                    >
                        <UndoIcon />
                    </IconButton>
                    <IconButton aria-label="delete" onClick={handleDelete}>
                        <DeleteIcon sx={IconButtonStyles} />
                    </IconButton>
                </Box>
                <Box sx={{ m: 4 }}>
                    <RenderedRequirementText text={editedText} />
                </Box>
            </Grid>
        </Grid>
    );
}
