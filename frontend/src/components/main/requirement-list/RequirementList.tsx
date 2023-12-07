import { useState } from "react";
import { Requirement } from "../../../types.ts";
import RequirementComponent from "./RequirementComponent.tsx";
import { List } from "@mui/material";

export default function RequirementList() {
    const [requirements, setRequirements] = useState<Requirement[]>([
        { id: "1", reviewed: true, text: "test text" },
        { id: "2", reviewed: false, text: "test text 2" },
    ]);
    return (
        <List>
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
