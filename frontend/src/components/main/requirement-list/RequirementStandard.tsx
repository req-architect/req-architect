import { Requirement } from "../../../types.ts";
import { IconButton, Typography } from "@mui/material";
import { useContext } from "react";
import { MainContext } from "../../../pages/MainPage.tsx";
import EditIcon from "@mui/icons-material/Edit";
import RenderedRequirementText from "./RenderedRequirementText.tsx";

export default function RequirementStandard({
    requirement,
}: {
    requirement: Requirement;
}) {
    const contextTools = useContext(MainContext);
    return (
        <>
            <Typography variant="h6" color="black" sx={{ mt: 10 }}>
                Requirement {requirement.id}
            </Typography>
            {contextTools?.isSelected(requirement) && (
                <IconButton aria-label="edit">
                    <EditIcon />
                </IconButton>
            )}
            <RenderedRequirementText text={requirement.text} />
        </>
    );
}
