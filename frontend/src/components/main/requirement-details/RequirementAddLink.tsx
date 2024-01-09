import { Autocomplete, Box, Button, Paper, TextField } from "@mui/material";
import { useCallback, useEffect, useState } from "react";
import {
    getAllRequirements,
    linkRequirement,
} from "../../../lib/api/requirementService";
import { Requirement, RequirementWithDoc } from "../../../types";
import { CUSTOM_ERROR_MESSAGES } from "../../../lib/api/fetchAPI";

interface RequirementsAndKey {
    allRequirements: RequirementWithDoc[];
    autocompleteKey: number;
}

export default function RequirementAddLink({
    requirement,
    refreshRequirements,
}: {
    requirement: Requirement;
    refreshRequirements: () => void;
}) {
    const [selectedRequirement, setSelectedRequirement] =
        useState<Requirement>();

    const [allRequirementsAndKey, setAllRequirementsAndKey] =
        useState<RequirementsAndKey>({
            allRequirements: [],
            autocompleteKey: 0,
        });

    const [errorState, setErrorState] = useState<string | null>(null);

    const filterRequirements = useCallback(
        (requirements: RequirementWithDoc[]) => {
            return requirements.filter((req) => {
                const isNotSelectedReq = req.id !== requirement.id;
                const isNotLinked = !requirement.links?.some(
                    (link) => link === req.id,
                );
                return isNotSelectedReq && isNotLinked;
            });
        },
        [requirement],
    );

    const fetchData = useCallback(async () => {
        try {
            const allReqs = await getAllRequirements();
            const filteredReqs = filterRequirements(allReqs.flat());
            setAllRequirementsAndKey({
                allRequirements: filteredReqs,
                autocompleteKey: allRequirementsAndKey.autocompleteKey + 1,
            });
        } catch (error) {
            console.error("Error fetching requirements:", error);
        }
    }, [filterRequirements]);

    useEffect(() => {
        fetchData().then();
        setErrorState(null);
    }, [fetchData, requirement]);

    const linkWithSelectedRequirement = async () => {
        if (!selectedRequirement) {
            setErrorState("No requirement selected");
            return;
        }
        try {
            await linkRequirement(requirement.id, selectedRequirement.id);
            refreshRequirements();
        } catch (error: any) {
            if (
                error.message.includes(CUSTOM_ERROR_MESSAGES.link_cycle_attempt)
            ) {
                setErrorState(
                    "Can't link this requirement - you mustn't build a cycle",
                );
            } else {
                throw error;
            }
            return;
        }
    };

    return (
        <Box mt={2}>
            <Autocomplete
                key={allRequirementsAndKey.autocompleteKey}
                options={allRequirementsAndKey.allRequirements}
                getOptionLabel={(option) => option.id}
                groupBy={(option) => option.docPrefix}
                onChange={(_event, newValue) =>
                    setSelectedRequirement(newValue || undefined)
                }
                PaperComponent={({ children }) => (
                    <Paper style={{ maxHeight: 160, overflow: "auto" }}>
                        {children}
                    </Paper>
                )}
                renderInput={(params) => (
                    <TextField
                        {...params}
                        error={!!errorState}
                        helperText={errorState}
                        label="Select Requirement"
                        sx={{ fontSize: "10px" }}
                    />
                )}
            />
            <Button
                onClick={linkWithSelectedRequirement}
                sx={{
                    mt: 1,
                    background: "green",
                    color: "white",
                    "&:hover": {
                        background: "#689F38",
                    },
                }}
            >
                Add Link
            </Button>
        </Box>
    );
}
