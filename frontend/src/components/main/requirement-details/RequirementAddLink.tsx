import { Autocomplete, Box, Button, TextField } from "@mui/material";
import { useContext, useEffect, useState } from "react";
import { MainContext } from "../../../pages/MainPage";
import {
    fetchRequirements,
    linkRequirement,
} from "../../../lib/api/requirementService";
import { fetchDocuments } from "../../../lib/api/documentService";
import { ReqDocumentWithChildren, Requirement } from "../../../types";

export default function RequirementAddLink() {
    const contextTools = useContext(MainContext);
    const [selectedRequirement, setSelectedRequirement] =
        useState<Requirement>();
    const [allRequirements, setAllRequirements] = useState<Requirement[]>([]);

    useEffect(() => {
        // Fetch all requirements except the selected one
        const fetchData = async () => {
            try {
                const documents = await fetchDocuments();
                const allReqs = await Promise.all(
                    documents.map(async (doc) => {
                        const reqs = await fetchRequirements(doc.prefix);
                        return reqs.concat(
                            await fetchChildRequirements(doc.children),
                        );
                    }),
                );
                const flattenedReqs = allReqs.flat();
                const filteredReqs = flattenedReqs.filter(
                    (req) =>
                        req.id !== contextTools?.data.selectedRequirement?.id,
                );
                setAllRequirements(filteredReqs);
            } catch (error) {
                console.error("Error fetching requirements:", error);
            }
        };

        const fetchChildRequirements = async (
            children?: ReqDocumentWithChildren[],
        ): Promise<Requirement[]> => {
            if (!children) {
                return [];
            }

            const childReqs = await Promise.all(
                children.map(async (child) => {
                    const reqs = await fetchRequirements(child.prefix);
                    return reqs.concat(
                        await fetchChildRequirements(child.children),
                    );
                }),
            );

            return childReqs.flat();
        };

        fetchData();
    }, [contextTools?.data.selectedRequirement]);

    const linkWithSelectedRequirement = async () => {
        if (!selectedRequirement) {
            console.log("No requirement selected");
            return;
        }
        if (!contextTools) {
            console.log("No context tools");
            return;
        }
        if (!contextTools.data.selectedRequirement) {
            console.log("No requirement to link to");
            return;
        }
        await linkRequirement(
            contextTools.data.selectedRequirement.id,
            selectedRequirement.id,
        );
        console.log("Linking requirement:", selectedRequirement);
    };

    return (
        <Box mt={2}>
            <Autocomplete
                options={allRequirements}
                getOptionLabel={(option) => option.id}
                renderInput={(params) => (
                    <TextField {...params} label="Select Requirement" />
                )}
                onChange={(_event, newValue) =>
                    setSelectedRequirement(newValue || undefined)
                }
            />
            <Button
                variant="outlined"
                onClick={linkWithSelectedRequirement}
                sx={{ mt: 1 }}
            >
                Add Link
            </Button>
        </Box>
    );
}
