import { Fab } from "@mui/material";
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
        <Fab
            size="small"
            color="success"
            aria-label="add"
            onClick={handleClick}
            sx={{mb: 2, mr: 2}}
        >
            <AddIcon />
        </Fab>
    );
}
