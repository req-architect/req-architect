import { Box, Button, Typography } from "@mui/material";
import RenderedRequirementText from "./RenderedRequirementText.tsx";
import { useMainContextTools } from "../../../hooks/useMainContext.ts";
import useRequirementContext from "../../../hooks/useRequirementContext.ts";

/*
    This component is used to display a requirement.
    It will display the requirement id and the requirement text.
    It will also allow the user to edit the requirement.
*/

export default function RequirementStandard() {
    const contextTools = useMainContextTools();
    const { requirement } = useRequirementContext();
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
            <Button
                onClick={() => {
                    contextTools.selectAndEdit(requirement.id);
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
