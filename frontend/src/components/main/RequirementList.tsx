import {ReqDocument, Requirement} from "../../types.ts";

export default function RequirementList({document, updateRequirement}: {document: ReqDocument | null, updateRequirement: (requirement: Requirement) => void}) {
    updateRequirement({id: '1', reviewed: true, text: 'test'})
    return (
        <p>Requirement List for {document?.prefix}</p>
    )
}