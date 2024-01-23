import { Fab } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { postRequirement } from "../../lib/api/requirementService.ts";
import { useMainContextTools } from "../../hooks/useMainContext.ts";
import useRepoContext from "../../hooks/useRepoContext.ts";
import { useAuth } from "../../hooks/useAuthContext.ts";
import { APIError } from "../../lib/api/fetchAPI.ts";
import { toast } from "react-toastify";

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
            )
                .then(refreshRequirements)
                .catch((e) => {
                    if (e instanceof APIError) {
                        toast.error(e.message);
                        return;
                    }
                    toast.error(
                        `An error occurred while trying to add requirement: ${e.name}`,
                    );
                    console.error(e);
                });
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
