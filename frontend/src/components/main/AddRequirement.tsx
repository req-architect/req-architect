import { Fab } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { postRequirement } from "../../lib/api/requirementService.ts";
import { useMainContextTools } from "../../hooks/useMainContext.ts";
import useRepoContext from "../../hooks/useRepoContext.ts";
import { useAuth } from "../../hooks/useAuthContext.ts";

/*
    This component is used to add a requirement.
    It will display a button to add a requirement.
    When the button is clicked, it will add a requirement to the current document.
*/

export default function AddRequirement({
    refreshRequirements,
}: {
    refreshRequirements: () => void;
}) {
    const mainContextTools = useMainContextTools();
    const authTools = useAuth();
    const repoTools = useRepoContext();
    async function handleClick() {
        if (!authTools.tokenStr || !repoTools.repositoryName) {
            return;
        }
        if (mainContextTools.data.selectedDocumentPrefix !== null) {
            await postRequirement(
                authTools.tokenStr,
                repoTools.repositoryName,
                mainContextTools.data.selectedDocumentPrefix,
            );
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
