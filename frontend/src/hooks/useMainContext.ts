import { useState } from "react";
import { ReqDocument, Requirement } from "../types.ts";

type MainContextData = {
    selectedDocument: ReqDocument | null;
    selectedRequirement: Requirement | null;
    editedRequirement: Requirement | null;
};

export type MainContextTools = {
    data: MainContextData;
    updateSelectedDocument: (document: ReqDocument) => void;
    updateSelectedRequirement: (requirement: Requirement) => void;
};
export default function useMainContext() {
    const [mainContext, setMainContext] = useState<MainContextData>({
        selectedDocument: null,
        selectedRequirement: null,
        editedRequirement: null,
    });
    function updateSelectedDocument(document: ReqDocument) {
        if (
            mainContext.editedRequirement !== null &&
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
            editedRequirement: null,
        }));
    }
    function updateSelectedRequirement(requirement: Requirement) {
        if (
            mainContext.editedRequirement !== null &&
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
            editedRequirement: null,
        }));
    }
    return {
        data: mainContext,
        updateSelectedDocument,
        updateSelectedRequirement,
    } as MainContextTools;
}
