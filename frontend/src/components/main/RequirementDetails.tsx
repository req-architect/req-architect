import {Requirement} from "../../types.ts";

export default function RequirementDetails({requirement}: {requirement: Requirement | null}) {
    return (
        <p>Requirement Details. Reviewed: {requirement?.reviewed}</p>
    )
}