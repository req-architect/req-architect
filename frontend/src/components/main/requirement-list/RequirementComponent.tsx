import { Requirement } from "../../../types";
import { Box } from "@mui/material";
import RequirementEditMode from "./RequirementEditMode.tsx";
import { useContext, useRef } from "react";
import { MainContext } from "../../../pages/MainPage.tsx";
import RequirementStandard from "./RequirementStandard.tsx";
import useClickInside from "../../../hooks/useClickInside.ts";

export default function RequirementComponent({
    requirement,
}: {
    requirement: Requirement;
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
                contextTools?.isSelected(requirement)
                    ? { outline: "2px solid green", marginBottom: 4 }
                    : { marginBottom: 4 }
            }
        >
            {/*Temporary button for testing*/}
            {contextTools?.isSelected(requirement) &&
            contextTools?.data.requirementEditMode ? (
                <RequirementEditMode requirement={requirement} />
            ) : (
                <RequirementStandard requirement={requirement} />
            )}
        </Box>
    );
}
