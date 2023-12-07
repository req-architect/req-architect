import React, { useState } from "react";
import { Requirement } from "../../../types.ts";
import { IconButton, TextField, Typography } from "@mui/material";
import RenderedRequirementText from "./RenderedRequirementText.tsx";
import UndoIcon from "@mui/icons-material/Undo";
import DoneIcon from "@mui/icons-material/Done";

export default function RequirementEditMode({
    requirement,
}: {
    requirement: Requirement;
}) {
    const [editedText, setEditedText] = useState(requirement.text);
    // const contextTools = useContext(MainContext);

    return (
        <>
            <Typography variant="h6" color="black" sx={{ mt: 10 }}>
                Requirement {requirement.id}
            </Typography>
            <IconButton aria-label="abort" color="error">
                <UndoIcon />
            </IconButton>
            <IconButton aria-label="save" color="success">
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
