import { useContext, useState } from "react";
import { MainContext } from "../pages/MainPage.tsx";

type MainContextData = {
    selectedDocumentPrefix: string | null;
    selectedRequirementId: string | null;
    requirementEditMode: boolean;
};

export type MainContextTools = {
    data: MainContextData;
    updateSelectedDocument: (documentPrefix: string | null) => void;
    updateSelectedRequirement: (requirementId: string | null) => void;
    updateEditMode: (editMode: boolean) => void;
    selectAndEdit: (requirementId: string) => void;
};
export default function useMainContext() {
    const [mainContext, setMainContext] = useState<MainContextData>({
        selectedDocumentPrefix: null,
        selectedRequirementId: null,
        requirementEditMode: false,
    });
    function updateSelectedDocument(documentPrefix: string | null) {
        if (
            mainContext.requirementEditMode &&
            mainContext.selectedDocumentPrefix !== documentPrefix
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
            selectedDocumentPrefix: documentPrefix,
            selectedRequirementId: null,
            requirementEditMode: false,
        }));
    }
    function updateSelectedRequirement(requirementId: string | null) {
        if (requirementId == mainContext.selectedRequirementId) return;
        if (
            mainContext.requirementEditMode &&
            mainContext.selectedRequirementId !== requirementId &&
            requirementId !== null
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
            selectedRequirementId: requirementId,
            requirementEditMode: false,
        }));
    }
    function updateEditMode(editMode: boolean) {
        setMainContext((prev) => ({
            ...prev,
            requirementEditMode: editMode,
        }));
    }
    function selectAndEdit(requirementId: string) {
        setMainContext((prev) => ({
            ...prev,
            selectedRequirementId: requirementId,
            requirementEditMode: true,
        }));
    }
    return {
        data: mainContext,
        updateSelectedDocument,
        updateSelectedRequirement,
        updateEditMode,
        selectAndEdit,
    } as MainContextTools;
}

export function useMainContextTools() {
    const contextTools = useContext(MainContext);
    if (contextTools === null) {
        throw new Error("MainContextTools is null");
    }
    return contextTools;
}
