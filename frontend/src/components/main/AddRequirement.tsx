import { Fab } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { postRequirement } from "../../lib/api/requirementService.ts";
import { useMainContextTools } from "../../hooks/useMainContext.ts";

export default function AddRequirement({
    refreshRequirements,
}: {
    refreshRequirements: () => void;
}) {
    const mainContextTools = useMainContextTools();
    async function handleClick() {
        if (mainContextTools.data.selectedDocumentPrefix !== null) {
            await postRequirement(mainContextTools.data.selectedDocumentPrefix);
            refreshRequirements();
        }
    }
    return (
        <Fab
            size="small"
            color="success"
            aria-label="add"
            onClick={handleClick}
            sx={{ mb: 2, mr: 2 }}
        >
            <AddIcon />
        </Fab>
    );
}
