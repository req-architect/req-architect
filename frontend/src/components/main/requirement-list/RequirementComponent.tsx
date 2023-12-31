import { Requirement } from "../../../types";
import { Box } from "@mui/material";
import RequirementEditMode from "./RequirementEditMode.tsx";
import { useRef } from "react";
import RequirementStandard from "./RequirementStandard.tsx";
import useClickInside from "../../../hooks/useClickInside.ts";
import Divider from "@mui/material/Divider";
import { useMainContextTools } from "../../../hooks/useMainContext.ts";

export default function RequirementComponent({
    requirement,
    refreshRequirements,
}: {
    requirement: Requirement;
    refreshRequirements: () => void;
}) {
    const contextTools = useMainContextTools();
    const wrapperRef = useRef<HTMLInputElement>(null);
    function handleSelect() {
        contextTools?.updateSelectedRequirement(requirement.id);
    }
    useClickInside(wrapperRef, handleSelect);
    return (
        <Box
            ref={wrapperRef}
            sx={
                contextTools.data.selectedRequirementId === requirement.id &&
                contextTools.data.requirementEditMode
                    ? {
                          outline: "1px solid green",
                          borderRadius: 2,
                          marginBottom: 4,
                          width: "100%",
                      }
                    : contextTools.data.selectedRequirementId === requirement.id
                      ? {
                            outline: "1px solid green",
                            borderRadius: 2,
                            marginBottom: 4,
                            width: "60%",
                        }
                      : { marginBottom: 4, width: "60%" }
            }
        >
            <Divider />
            {contextTools.data.selectedRequirementId === requirement.id &&
            contextTools?.data.requirementEditMode ? (
                <RequirementEditMode
                    requirement={requirement}
                    refreshRequirements={refreshRequirements}
                />
            ) : (
                <RequirementStandard requirement={requirement} />
            )}
        </Box>
    );
}
