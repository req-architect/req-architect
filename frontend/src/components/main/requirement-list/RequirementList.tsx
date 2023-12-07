import { useContext, useEffect, useState } from "react";
import { List, Box } from "@mui/material";
import { MainContext } from "../../../pages/MainPage.tsx";
import { Requirement } from "../../../types.ts";
import RequirementComponent from "./RequirementComponent.tsx";

export default function RequirementList() {
    const [requirements, setRequirements] = useState<Requirement[]>([
        { id: "1", reviewed: true, text: "test text" },
    ]);
    const contextTools = useContext(MainContext);
    useEffect(() => {
        contextTools?.updateSelectedRequirement({
            id: "1",
            reviewed: true,
            text: "test text",
        });
    }, [contextTools]);
    const document = contextTools?.data.selectedDocument;
    return (
        <List>
            <Box>Document {document?.prefix}</Box>
            {requirements.map((requirement) => (
                <RequirementComponent requirement={requirement} />
            ))}
        </List>
    );
}

// export default function RequirementList({document, updateRequirement}: {document: ReqDocument | null, updateRequirement: (requirement: Requirement) => void}) {
//     useEffect(() => {
//         updateRequirement({id: '1', reviewed: true, text: 'test'})
//     }, [updateRequirement]);
//     return (
//         <p>Requirement List for {document?.prefix}</p>
//     )
// }
