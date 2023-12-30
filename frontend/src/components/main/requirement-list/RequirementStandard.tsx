import { Requirement } from "../../../types.ts";
import { Box, Button, Typography } from "@mui/material";
import RenderedRequirementText from "./RenderedRequirementText.tsx";
import { useMainContextTools } from "../../../hooks/useMainContext.ts";

export default function RequirementStandard({
    requirement,
}: {
    requirement: Requirement;
}) {
    const contextTools = useMainContextTools();
    function handleSelect() {
        contextTools.updateSelectedRequirement(requirement.id);
    }
    return (
        <Box sx={{ m: 2 }}>
            <Typography
                variant="h6"
                color="black"
                fontWeight={"bold"}
                sx={{ mb: 1 }}
            >
                Req {requirement.id}
            </Typography>
            <RenderedRequirementText text={requirement.text} />
            {/* {contextTools?.isSelected(requirement) && (
                <IconButton
                    aria-label="edit"
                    onClick={() => contextTools?.updateEditMode(true)}
                >
                    <EditIcon />
                </IconButton>
            )} */}
            <Button
                onClick={() => {
                    handleSelect();
                    contextTools.updateEditMode(true);
                }}
                sx={{
                    background: "green",
                    color: "white",
                    width: "60px",
                    height: "30px",
                    mt: 2,
                    "&:hover": {
                        background: "#689F38",
                    },
                    textTransform: "none",
                }}
            >
                Edit
            </Button>
        </Box>
    );
}
