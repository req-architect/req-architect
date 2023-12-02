import MainPageHeader from "../components/MainPageHeader.tsx";
import DocumentList from "../components/DocumentList.tsx";
import RequirementList from "../components/RequirementList.tsx";
import RequirementDetails from "../components/RequirementDetails.tsx";
import {useState} from "react";
import {ReqDocument, Requirement} from "../types.ts";

export default function MainPage() {
    const [ selectedDocReq, setSelectedDocReq ] = useState<[ReqDocument | null, Requirement | null]>([null, null])
    function updateDocument(document: ReqDocument) {
        setSelectedDocReq([document, null])
    }
    function updateRequirement(requirement: Requirement) {
        setSelectedDocReq(prev => [prev[0], requirement])
    }
    return (
        <>
            <MainPageHeader/>
            <DocumentList updateDocument={updateDocument}/>
            <RequirementList document={selectedDocReq[0]} updateRequirement={updateRequirement}/>
            <RequirementDetails requirement={selectedDocReq[1]}/>
        </>
    )
}
