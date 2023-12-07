import { Requirement } from "../../../types";
import { Box } from "@mui/material";
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
    return (
        // add an outline to box if it is selected
        // TODO: change width of the box if selected && edit mode
        <Box
            sx={
                contextTools?.isSelected(requirement)
                    ? { outline: "1px solid green" }
                    : {}
            }
        >
            {contextTools?.isSelected(requirement) &&
            contextTools?.data.requirementEditMode ? (
                <RequirementEditMode requirement={requirement} />
            ) : (
                <RequirementStandard requirement={requirement} />
            )}
        </Box>
    );
}
