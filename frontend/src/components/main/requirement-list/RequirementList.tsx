import { Requirement } from "../../../types.ts";
import RequirementComponent from "./RequirementComponent.tsx";
import { List, Box } from "@mui/material";

export default function RequirementList({
    requirements,
    updateRequirements,
}: {
    requirements: Requirement[];
    updateRequirements: () => void;
}) {
    // const [requirements, setRequirements] = useState<Requirement[]>([
    //     { id: "1", reviewed: true, text: "System shall provide feature 1" },
    //     { id: "2", reviewed: false, text: "System shall provide feature 2" },
    //     { id: "3", reviewed: false, text: "System shall provide feature 3" },
    //     { id: "4", reviewed: false, text: "System shall provide feature 4" },
    //     { id: "5", reviewed: true, text: "System shall provide feature 5" },
    //     { id: "6", reviewed: false, text: "System shall provide feature 6" },
    //     { id: "7", reviewed: false, text: "System shall provide feature 7" },
    // ]);
    return (
        <List>
            {requirements.map((requirement) => (
                <Box sx={{display: "flex",  justifyContent: "center"}}>
                    <RequirementComponent
                        requirement={requirement}
                        updateRequirements={updateRequirements}
                    />
                </Box>
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
