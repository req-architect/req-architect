import {
    Box,
    IconButton,
    List,
    ListItem,
    ListItemText,
    Typography,
} from "@mui/material";
import LinkIcon from "@mui/icons-material/Link";
import DeleteIcon from "@mui/icons-material/Delete";
import RequirementAddLink from "./RequirementAddLink.tsx";
import { unlinkRequirement } from "../../../lib/api/requirementService";
import { IconButtonStyles } from "../../../lib/styles.ts";
import { Requirement } from "../../../types.ts";
import useRepoContext from "../../../hooks/useRepoContext.ts";
import { useAuth } from "../../../hooks/useAuthContext.ts";
import { APIError } from "../../../lib/api/fetchAPI.ts";
import { toast } from "react-toastify";

/*
    This component is used to display the details of a requirement.
    It will display the requirement id, whether it is reviewed or not and the links it has.
    It will also allow the user to unlink a requirement from the current requirement.
*/

export default function RequirementDetails({
    requirement,
    refreshRequirements,
}: {
    requirement: Requirement | null;
    refreshRequirements: () => void;
}) {
    const authTools = useAuth();
    const repoTools = useRepoContext();

    const unlinkSelectedRequirement = async (linkReqId: string) => {
        if (!authTools.tokenStr || !repoTools.repositoryName) {
            return;
        }
        if (requirement) {
            await unlinkRequirement(
                authTools.tokenStr,
                repoTools.repositoryName,
                requirement.id,
                linkReqId,
            )
                .then(refreshRequirements)
                .catch((e) => {
                    if (e instanceof APIError) {
                        if (e.api_error_code == "INVALID_TOKEN") {
                            authTools.logout(e.message);
                            return;
                        }
                        toast.error(e.message);
                        return;
                    }
                    toast.error(
                        `An error occurred while trying to unlink requirements: ${e.name}`,
                    );
                    console.error(e);
                });
        }
    };

    return (
        <Box
            borderLeft="1px solid green"
            sx={{
                p: 2,
                // width: "15%",
                height: "100%",
            }}
        >
            {requirement && (
                <Box>
                    <Box textAlign="center">
                        <Typography variant="h5" fontWeight="bold" mb={1}>
                            {requirement.id}
                        </Typography>
                        <Typography sx={{ mt: 1 }}>
                            Reviewed: {requirement.reviewed ? "Yes" : "No"}
                        </Typography>
                    </Box>
                    <Typography variant="h6" fontWeight="bold">
                        Links:
                    </Typography>
                    <Box>
                        {requirement.links.length > 0 ? (
                            <List>
                                {requirement.links.map((linkText, index) => (
                                    <ListItem key={index}>
                                        <LinkIcon
                                            fontSize="small"
                                            sx={{ marginRight: 1 }}
                                        />
                                        <ListItemText primary={linkText} />
                                        <IconButton
                                            edge="end"
                                            aria-label="delete"
                                            sx={IconButtonStyles}
                                            onClick={() =>
                                                unlinkSelectedRequirement(
                                                    linkText,
                                                )
                                            }
                                        >
                                            <DeleteIcon />
                                        </IconButton>
                                    </ListItem>
                                ))}
                            </List>
                        ) : (
                            <Typography>No links</Typography>
                        )}
                    </Box>
                    <RequirementAddLink
                        requirement={requirement}
                        refreshRequirements={refreshRequirements}
                    />
                </Box>
            )}
        </Box>
    );
}
