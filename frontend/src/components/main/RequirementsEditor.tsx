import Grid from "@mui/material/Grid";
import { Box } from "@mui/material";
import RequirementList from "./requirement-list/RequirementList.tsx";
import AddRequirement from "./AddRequirement.tsx";
import RequirementDetails from "./RequirementDetails.tsx";
import { useEffect, useState } from "react";
import { Requirement } from "../../types.ts";
import { fetchRequirements } from "../../lib/api/requirementService.ts";
import { useMainContextTools } from "../../hooks/useMainContext.ts";

export default function RequirementsEditor() {
    const mainContextTools = useMainContextTools();
    const [fetchedRequirements, setFetchedRequirements] = useState<
        Requirement[]
    >([]);
    async function refreshRequirements() {
        if (mainContextTools.data.selectedDocumentPrefix !== null) {
            const data = await fetchRequirements(
                mainContextTools.data.selectedDocumentPrefix,
            );
            console.log("Fetched requirements:", data);
            setFetchedRequirements(data);
        }
    }
    useEffect(() => {
        refreshRequirements();
    }, [mainContextTools.data.selectedDocumentPrefix]);

    function findRequirement(id: string | null) {
        return fetchedRequirements.find((req) => req.id === id) || null;
    }
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
                        mainContextTools.data.selectedRequirementId,
                    )}
                />
            </Grid>
        </>
    );
}
