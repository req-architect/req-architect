import { Autocomplete, Box, Button, Paper, TextField } from "@mui/material";
import { useCallback, useEffect, useState } from "react";
import {
    getAllRequirements,
    linkRequirement,
} from "../../../lib/api/requirementService";
import { Requirement, RequirementWithDoc } from "../../../types";

type ErrorState = {
    prefixError: string | null;
    parentPrefixError: string | null;
};

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

    const [errorState, setErrorState] = useState<ErrorState>({
        prefixError: null,
        parentPrefixError: null,
    });

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
        let newErrorState: ErrorState = {
            prefixError: null,
            parentPrefixError: null,
        };
        setErrorState(newErrorState);
    }, [fetchData, requirement]);

    const linkWithSelectedRequirement = async () => {
        let newErrorState: ErrorState = {
            prefixError: null,
            parentPrefixError: null,
        };
        if (!selectedRequirement) {
            newErrorState = {
                ...newErrorState,
                prefixError: "No requirement selected",
            };
            setErrorState(newErrorState);
            return;
        }
        if (!requirement) {
            console.log("No requirement is selected");
            return;
        }
        try {
            await linkRequirement(requirement.id, selectedRequirement.id);
            refreshRequirements();
        } catch (error) {
            console.clear();
            newErrorState = {
                ...newErrorState,
                prefixError:
                    "Can't link this requirement - you mustn't build a cycle",
            };
        }
        setErrorState(newErrorState);
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
                        error={!!errorState.prefixError}
                        helperText={errorState.prefixError}
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
