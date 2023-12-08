import { useState } from "react";
import { ReqDocument, Requirement } from "../types.ts";

type MainContextData = {
    selectedDocument: ReqDocument | null;
    selectedRequirement: Requirement | null;
    requirementEditMode: boolean;
};

export type MainContextTools = {
    data: MainContextData;
    updateSelectedDocument: (document: ReqDocument) => void;
    updateSelectedRequirement: (requirement: Requirement) => void;
    updateEditMode: (editMode: boolean) => void;
    isSelected: (requirement: Requirement) => boolean;
};
export default function useMainContext() {
    const [mainContext, setMainContext] = useState<MainContextData>({
        selectedDocument: { prefix: "REQ" },
        selectedRequirement: null,
        requirementEditMode: false,
    });
    function updateSelectedDocument(document: ReqDocument) {
        if (
            mainContext.requirementEditMode &&
            mainContext.selectedDocument !== document
        ) {
            if (
                !confirm(
                    "Are you sure you want to leave this page? All unsaved changes will be lost.",
                )
            ) {
                return;
            }
        }
        setMainContext((prev) => ({
            ...prev,
            selectedDocument: document,
            selectedRequirement: null,
            requirementEditMode: false,
        }));
    }
    function updateSelectedRequirement(requirement: Requirement) {
        if (
            mainContext.requirementEditMode &&
            mainContext.selectedRequirement !== requirement
        ) {
            if (
                !confirm(
                    "Are you sure you want to leave this page? All unsaved changes will be lost.",
                )
            ) {
                return;
            }
        }
        setMainContext((prev) => ({
            ...prev,
            selectedRequirement: requirement,
            requirementEditMode: false,
        }));
    }
    function updateEditMode(editMode: boolean) {
        setMainContext((prev) => ({
            ...prev,
            requirementEditMode: editMode,
        }));
    }
    function isSelected(requirement: Requirement) {
        return mainContext.selectedRequirement === requirement;
    }
    return {
        data: mainContext,
        updateSelectedDocument,
        updateSelectedRequirement,
        updateEditMode,
        isSelected,
    } as MainContextTools;
}
