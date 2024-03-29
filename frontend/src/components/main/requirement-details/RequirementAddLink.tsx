import { Autocomplete, Box, Button, Paper, TextField } from "@mui/material";
import { useCallback, useEffect, useState } from "react";
import {
    getAllRequirements,
    linkRequirement,
} from "../../../lib/api/requirementService";
import { Requirement, RequirementWithDoc } from "../../../types";
import { APIError } from "../../../lib/api/fetchAPI";
import useRepoContext from "../../../hooks/useRepoContext.ts";
import { useAuth } from "../../../hooks/useAuthContext.ts";
import { toast } from "react-toastify";

/*
    This component is used to add a link to a requirement.
    It will fetch all the requirements from the API and display them in a dropdown (minus the chosen requirement and requirements already linked).
    The user will then be able to select a requirement and link it to the current requirement.
*/

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
    const authTools = useAuth();
    const repoTools = useRepoContext();
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
        if (!authTools.tokenStr || !repoTools.repositoryName) {
            return;
        }
        await getAllRequirements(authTools.tokenStr, repoTools.repositoryName)
            .then((allReqs) => {
                const filteredReqs = filterRequirements(allReqs.flat());
                setAllRequirementsAndKey((prevAllRequirementsAndKey) => ({
                    allRequirements: filteredReqs,
                    autocompleteKey:
                        prevAllRequirementsAndKey.autocompleteKey + 1,
                }));
            })
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
                    `An error occurred while fetching requirements: ${e.name}`,
                );
                console.error(e);
            });
    }, [authTools, repoTools, filterRequirements]);

    useEffect(() => {
        fetchData().then();
        setErrorState(null);
    }, [fetchData, requirement]);

    const linkWithSelectedRequirement = async () => {
        if (!selectedRequirement) {
            setErrorState("No requirement selected");
            return;
        }
        if (!authTools.tokenStr || !repoTools.repositoryName) {
            return;
        }
        await linkRequirement(
            authTools.tokenStr,
            repoTools.repositoryName,
            requirement.id,
            selectedRequirement.id,
        )
            .then(refreshRequirements)
            .catch((e) => {
                if (e instanceof APIError) {
                    if (e.api_error_code == "INVALID_TOKEN") {
                        authTools.logout(e.message);
                        return;
                    }
                    if (e.api_error_code == "LINK_CYCLE_ATTEMPT") {
                        setErrorState(
                            "Can't link this requirement - you mustn't build a cycle",
                        );
                        return;
                    }
                    toast.error(e.message);
                    return;
                }
                toast.error(
                    `An error occurred while trying to link requirements: ${e.name}`,
                );
                console.error(e);
            });
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
