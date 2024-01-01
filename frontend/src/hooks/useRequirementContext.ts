import { Requirement } from "../types.ts";
import { useContext } from "react";
import { RequirementContext } from "../components/main/requirement-list/RequirementList.tsx";

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
