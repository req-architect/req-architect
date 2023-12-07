import {Requirement} from "../../types.ts";
import Grid from "@mui/material/Grid";

export default function RequirementDetails({requirement}: {requirement: Requirement | null}) {
    return (
        <Grid
            container
            borderLeft="1px solid green"
            sx={{
                p: 0,
                justifyContent: "center",
                // width: "15%",
                height: "100%",
            }}
        >
            Requirement Details. Reviewed: {requirement?.reviewed}
        </Grid>
    )
}