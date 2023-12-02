import {ReqDocument, Requirement} from "../types.ts";

export default function RequirementList({document, updateRequirement}: {document: ReqDocument | null, updateRequirement: (requirement: Requirement) => void}) {
    return (
        <p>Requirement List</p>
    )
}