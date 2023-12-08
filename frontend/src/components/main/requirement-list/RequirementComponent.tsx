import { Requirement } from "../../../types";
import { Box, Button } from "@mui/material";
import RequirementEditMode from "./RequirementEditMode.tsx";
import { useContext } from "react";
import { MainContext } from "../../../pages/MainPage.tsx";
import RequirementStandard from "./RequirementStandard.tsx";

export default function RequirementComponent({
    requirement,
}: {
    requirement: Requirement;
}) {
    const contextTools = useContext(MainContext);
    function handleSelect() {
        contextTools?.updateSelectedRequirement(requirement);
    }
    return (
        // add an outline to box if it is selected
        // TODO: change width of the box if selected && edit mode
        <Box
            sx={
                contextTools?.isSelected(requirement)
                    ? { border: "1px solid green" }
                    : {}
            }
        >
            {/*Temporary button for testing*/}
            <Button onClick={handleSelect}>SELECT</Button>
            {contextTools?.isSelected(requirement) &&
            contextTools?.data.requirementEditMode ? (
                <RequirementEditMode requirement={requirement} />
            ) : (
                <RequirementStandard requirement={requirement} />
            )}
        </Box>
    );
}
