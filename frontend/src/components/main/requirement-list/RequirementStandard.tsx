import { Requirement } from "../../../types.ts";
import { IconButton, Typography, Button, Box } from "@mui/material";
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
    function handleSelect() {
        contextTools?.updateSelectedRequirement(requirement);
    }
    return (
        <Box sx={{m: 2}}>
            <Typography variant="h6" color="black" sx={{mt: 1}}>
                Req {requirement.id}
            </Typography>
            <RenderedRequirementText text={requirement.text}/>
            {/* {contextTools?.isSelected(requirement) && (
                <IconButton
                    aria-label="edit"
                    onClick={() => contextTools?.updateEditMode(true)}
                >
                    <EditIcon />
                </IconButton>
            )} */}
            <Button
                onClick={() => {handleSelect(); contextTools?.updateEditMode(true);}}
                sx={{
                    background: "green",
                    color: "white",
                    minWidth: "80px",
                    height: "40px",
                    mt: 2,
                    "&:hover": {
                        background: "#689F38",
                    },
                    textTransform: "none",
                }}
                >EDIT
            </Button>
        </Box>
    );
}
