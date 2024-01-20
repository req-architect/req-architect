import { useContext, useState } from "react";
import { MainContext } from "../pages/MainPage.tsx";
import { defaultConfirm } from "../lib/defaultConfirm.ts";

/* 
    This hook is used to manage the main context of the application.
    It is used to manage the selected document and requirement.
    It also provides functions to update the context.
*/

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
        function checkAndUpdate() {
            setMainContext((prev) =>
                prev.selectedDocumentPrefix === documentPrefix
                    ? prev
                    : {
                          ...prev,
                          selectedDocumentPrefix: documentPrefix,
                          selectedRequirementId: null,
                          requirementEditMode: false,
                      },
            );
        }
        if (
            mainContext.requirementEditMode &&
            mainContext.selectedDocumentPrefix !== documentPrefix
        ) {
            defaultConfirm(
                "Abort confirmation",
                "You are currently editing a requirement. Are you sure you want to leave this page?",
                () => {
                    checkAndUpdate();
                },
            );
            return;
        }
        checkAndUpdate();
    }
    function updateSelectedRequirement(requirementId: string | null) {
        function checkAndUpdate() {
            setMainContext((prev) =>
                prev.selectedRequirementId === requirementId
                    ? prev
                    : {
                          ...prev,
                          selectedRequirementId: requirementId,
                          requirementEditMode: false,
                      },
            );
        }
        if (requirementId == mainContext.selectedRequirementId) return;
        if (
            mainContext.requirementEditMode &&
            mainContext.selectedRequirementId !== requirementId &&
            requirementId !== null
        ) {
            defaultConfirm(
                "Abort confirmation",
                "You are currently editing a requirement. Are you sure you want to leave this page?",
                () => {
                    checkAndUpdate();
                },
            );
            return;
        }
        checkAndUpdate();
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
