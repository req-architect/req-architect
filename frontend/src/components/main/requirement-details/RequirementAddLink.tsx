import { Autocomplete, Box, Button, Paper, TextField } from "@mui/material";
import {useCallback, useEffect, useState} from "react";
import {
    fetchRequirements,
    linkRequirement,
} from "../../../lib/api/requirementService";
import { fetchDocuments } from "../../../lib/api/documentService";
import {
    ReqDocumentWithChildren,
    Requirement,
    RequirementWithDoc,
} from "../../../types";

const fetchChildRequirements = async (
    children?: ReqDocumentWithChildren[],
): Promise<RequirementWithDoc[]> => {
    if (!children) {
        return [];
    }

    const childReqs = await Promise.all(
        children.map(async (child) => {
            const reqs = await fetchRequirements(child.prefix);
            const reqsWithDoc: RequirementWithDoc[] = reqs.map((req) => ({
                ...req,
                docPrefix: child.prefix,
            }));
            return reqsWithDoc.concat(
                await fetchChildRequirements(child.children),
            );
        }),
    );
    return childReqs.flat();
};

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
            const documents = await fetchDocuments();
            const allReqs = await Promise.all(
                documents.map(async (doc) => {
                    const prefix = doc.prefix;
                    const reqs = await fetchRequirements(prefix);
                    const reqsWithDoc: RequirementWithDoc[] = reqs.map(
                        (req) => ({
                            ...req,
                            docPrefix: prefix,
                        }),
                    );
                    return reqsWithDoc.concat(
                        await fetchChildRequirements(doc.children),
                    );
                }),
            );
            const flattenedReqs = allReqs.flat();
            const filteredReqs = filterRequirements(flattenedReqs);
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
