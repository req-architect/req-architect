import Grid from "@mui/material/Grid";
import { Box } from "@mui/material";
import RequirementList from "./requirement-list/RequirementList.tsx";
import AddRequirement from "./AddRequirement.tsx";
import RequirementDetails from "./requirement-details/RequirementDetails.tsx";
import { useCallback, useEffect, useState } from "react";
import { Requirement } from "../../types.ts";
import { fetchRequirements } from "../../lib/api/requirementService.ts";
import { useMainContextTools } from "../../hooks/useMainContext.ts";
import { useAuth } from "../../hooks/useAuthContext.ts";
import useRepoContext from "../../hooks/useRepoContext.ts";

function findRequirement(requirements: Requirement[], id: string | null) {
    return requirements.find((req) => req.id === id) || null;
}
export default function RequirementsEditor() {
    const mainContextTools = useMainContextTools();
    const [fetchedRequirements, setFetchedRequirements] = useState<
        Requirement[]
    >([]);
    const authTools = useAuth();
    const repoTools = useRepoContext();
    const refreshRequirements = useCallback(async () => {
        if (!authTools.tokenStr || !repoTools.repositoryName) {
            return;
        }
        if (mainContextTools.data.selectedDocumentPrefix !== null) {
            const data = await fetchRequirements(
                authTools.tokenStr,
                repoTools.repositoryName,
                mainContextTools.data.selectedDocumentPrefix,
            );
            console.log("Fetched requirements:", data);
            setFetchedRequirements(data);
        }
    }, [authTools, repoTools, mainContextTools.data.selectedDocumentPrefix]);

    useEffect(() => {
        refreshRequirements().then();
    }, [refreshRequirements]);

    useEffect(() => {
        if (mainContextTools.data.selectedRequirementId) {
            if (
                !findRequirement(
                    fetchedRequirements,
                    mainContextTools.data.selectedRequirementId,
                )
            ) {
                mainContextTools.updateSelectedRequirement(null);
            }
        }
    }, [mainContextTools, fetchedRequirements]);

    return (
        <>
            <Grid
                item
                xs={8}
                sx={{
                    height: "100%",
                }}
            >
                {mainContextTools.data.selectedDocumentPrefix && (
                    <>
                        <Box sx={{ height: "100%", overflowY: "auto" }}>
                            <RequirementList
                                requirements={fetchedRequirements}
                                refreshRequirements={refreshRequirements}
                            />
                        </Box>
                        <Box
                            sx={{
                                height: "0%",
                                display: "flex",
                                justifyContent: "flex-end",
                                alignItems: "flex-end",
                            }}
                        >
                            <AddRequirement
                                refreshRequirements={refreshRequirements}
                            />
                        </Box>
                    </>
                )}
            </Grid>
            <Grid item xs={2}>
                <RequirementDetails
                    requirement={findRequirement(
                        fetchedRequirements,
                        mainContextTools.data.selectedRequirementId,
                    )}
                    refreshRequirements={refreshRequirements}
                />
            </Grid>
        </>
    );
}
