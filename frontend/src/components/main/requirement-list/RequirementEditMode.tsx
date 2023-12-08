import React, { useContext, useState } from "react";
import { Requirement } from "../../../types.ts";
import { IconButton, TextField, Typography } from "@mui/material";
import RenderedRequirementText from "./RenderedRequirementText.tsx";
import UndoIcon from "@mui/icons-material/Undo";
import DoneIcon from "@mui/icons-material/Done";
import { MainContext } from "../../../pages/MainPage.tsx";

export default function RequirementEditMode({
    requirement,
}: {
    requirement: Requirement;
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
    }
    function handleSave() {
        // TODO: update requirement in database and reload
        contextTools?.updateEditMode(false);
    }
    return (
        <>
            <Typography variant="h6" color="black" sx={{ mt: 10 }}>
                {requirement.id}
            </Typography>
            <IconButton aria-label="abort" color="error" onClick={handleAbort}>
                <UndoIcon />
            </IconButton>
            <IconButton aria-label="save" color="success" onClick={handleSave}>
                <DoneIcon />
            </IconButton>
            <TextField
                multiline
                rows={4}
                value={editedText}
                onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                    setEditedText(event.target.value);
                }}
                sx={{ width: "100%", mt: 2 }}
            />

            <RenderedRequirementText text={editedText} />
        </>
    );
}
