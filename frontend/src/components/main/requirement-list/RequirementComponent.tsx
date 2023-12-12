import { Requirement } from "../../../types";
import { Box } from "@mui/material";
import RequirementEditMode from "./RequirementEditMode.tsx";
import { useContext, useRef } from "react";
import { MainContext } from "../../../pages/MainPage.tsx";
import RequirementStandard from "./RequirementStandard.tsx";
import useClickInside from "../../../hooks/useClickInside.ts";
import Divider from "@mui/material/Divider";

export default function RequirementComponent({
    requirement,
    updateRequirements,
}: {
    requirement: Requirement;
    updateRequirements: () => void;
}) {
    const contextTools = useContext(MainContext);
    const wrapperRef = useRef<HTMLInputElement>(null);
    function handleSelect() {
        contextTools?.updateSelectedRequirement(requirement);
    }
    useClickInside(wrapperRef, handleSelect);
    return (
        // add an outline to box if it is selected
        // TODO: change width of the box if selected && edit mode
        <Box
            ref={wrapperRef}
            sx={
                contextTools?.isSelected(requirement) && 
                contextTools?.data.requirementEditMode
                    ? { outline: "1px solid green", borderRadius: 2, marginBottom: 4, width: "100%" }
                    : contextTools?.isSelected(requirement) ? { outline: "1px solid green", borderRadius: 2, marginBottom: 4, width: "60%"}
                    : { marginBottom: 4, width: "60%" }
            }
        >
            <Divider />
            {/*Temporary button for testing*/}
            {contextTools?.isSelected(requirement) &&
            contextTools?.data.requirementEditMode ? (
                <RequirementEditMode
                    requirement={requirement}
                    updateRequirements={updateRequirements}
                />
            ) : (
                <RequirementStandard requirement={requirement} />
            )}
        </Box>
    );
}
