import { Requirement } from "../types.ts";
import { useContext } from "react";
import { RequirementContext } from "../components/main/requirement-list/RequirementList.tsx";

/*
    This hook is used to manage the requirement context of the application.
    It is used to manage the selected requirement.
    It also provides functions to update the context.
*/

export type RequirementContextType = {
    requirement: Requirement;
    refreshRequirements: () => void;
};

export default function useRequirementContext(): RequirementContextType {
    const context = useContext(RequirementContext);
    if (!context) {
        throw new Error(
            "useRequirementContext must be used within a RequirementContextProvider",
        );
    }
    return context;
}
