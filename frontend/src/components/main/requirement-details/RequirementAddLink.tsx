import { Autocomplete, Box, Button, Paper, TextField } from "@mui/material";
import {useCallback, useEffect, useState} from "react";
import {
    getAllRequirements,
    linkRequirement,
} from "../../../lib/api/requirementService";
import {Requirement, RequirementWithDoc} from "../../../types";

export default function RequirementAddLink({requirement, refreshRequirements}: {requirement: Requirement, refreshRequirements: () => void}) {
    const [selectedRequirement, setSelectedRequirement] =
        useState<Requirement>();
    const [allRequirements, setAllRequirements] = useState<
        RequirementWithDoc[]
    >([]);
    const [autocompleteKey, setAutocompleteKey] = useState(0);

    const filterRequirements = useCallback((requirements: RequirementWithDoc[]) => {

        return requirements.filter((req) => {
            const isNotSelectedReq = req.id !== requirement.id;
            const isNotLinked = !requirement.links?.some(
                (link) => link === req.id,
            );
            return isNotSelectedReq && isNotLinked;
        });
    }, [requirement]);

    const fetchData = useCallback(async () => {
        try {
            const allReqs = await getAllRequirements();
            const filteredReqs = filterRequirements(allReqs.flat());
            setAllRequirements(filteredReqs);
            setAutocompleteKey((prevKey) => prevKey + 1);
        } catch (error) {
            console.error("Error fetching requirements:", error);
        }
    }, [filterRequirements]);

    useEffect(() => {
        fetchData().then();
    }, [
        fetchData,
        requirement
    ]);

    const linkWithSelectedRequirement = async () => {
        if (!selectedRequirement) {
            console.log("No requirement selected");
            return;
        }
        if (!requirement) {
            console.log("No requirement to link to");
            return;
        }
        await linkRequirement(
            requirement.id,
            selectedRequirement.id,
        );
        refreshRequirements();
    };

    return (
        <Box mt={2}>
            <Autocomplete
                key={autocompleteKey}
                options={allRequirements}
                getOptionLabel={(option) => option.id}
                groupBy={(option) => option.docPrefix}
                renderInput={(params) => (
                    <TextField
                        {...params}
                        label="Select Requirement"
                        sx={{ fontSize: "10px" }}
                    />
                )}
                onChange={(_event, newValue) =>
                    setSelectedRequirement(newValue || undefined)
                }
                PaperComponent={({ children }) => (
                    <Paper style={{ maxHeight: 160, overflow: "auto" }}>
                        {children}
                    </Paper>
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
