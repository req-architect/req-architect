import Grid from "@mui/material/Grid";
import { Box } from "@mui/material";
import RequirementList from "./requirement-list/RequirementList.tsx";
import AddRequirement from "./AddRequirement.tsx";
import RequirementDetails from "./RequirementDetails.tsx";
import { useCallback, useEffect, useState } from "react";
import { Requirement } from "../../types.ts";
import { fetchRequirements } from "../../lib/api/requirementService.ts";
import { useMainContextTools } from "../../hooks/useMainContext.ts";

function findRequirement(requirements: Requirement[], id: string | null) {
    return requirements.find((req) => req.id === id) || null;
}
export default function RequirementsEditor() {
    const mainContextTools = useMainContextTools();
    const [fetchedRequirements, setFetchedRequirements] = useState<
        Requirement[]
    >([]);

    const refreshRequirements = useCallback(async () => {
        if (mainContextTools.data.selectedDocumentPrefix !== null) {
            const data = await fetchRequirements(
                mainContextTools.data.selectedDocumentPrefix,
            );
            console.log("Fetched requirements:", data);
            setFetchedRequirements(data);
        }
    }, [mainContextTools.data.selectedDocumentPrefix]);

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
                />
            </Grid>
        </>
    );
}
