import {ReqDocument, Requirement} from "../../types.ts";
import {useEffect} from "react";

export default function RequirementList({document, updateRequirement}: {document: ReqDocument | null, updateRequirement: (requirement: Requirement) => void}) {
    useEffect(() => {
        updateRequirement({id: '1', reviewed: true, text: 'test'})
    }, [updateRequirement]);
    return (
        <p>Requirement List for {document?.prefix}</p>
    )
}