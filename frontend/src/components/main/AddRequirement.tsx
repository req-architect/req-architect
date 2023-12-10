import { Fab, Grid } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { postRequirement } from "../../lib/api/requirementService.ts";

export default function AddRequirement({
    docPrefix,
    updateRequirements,
}: {
    docPrefix: string;
    updateRequirements: () => void;
}) {
    async function handleClick() {
        await postRequirement(docPrefix);
        updateRequirements();
    }
    return (
        <Grid item container justifyContent={"flex-end"} mt={2} height={"10vh"}>
            <Fab
                size="small"
                color="success"
                aria-label="add"
                sx={{ ml: "auto", mr: 8, mb: 2 }}
                onClick={handleClick}
            >
                <AddIcon />
            </Fab>
        </Grid>
    );
}
