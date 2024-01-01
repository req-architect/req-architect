import Grid from "@mui/material/Grid";
import { Typography } from "@mui/material";
import { Requirement } from "../../types.ts";

export default function RequirementDetails({
    requirement,
}: {
    requirement: Requirement | null;
}) {
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
            {requirement && (
                <Typography>
                    Requirement Details. Reviewed:{" "}
                    {requirement.reviewed ? "Yes" : "No"}
                </Typography>
            )}
        </Grid>
    );
}
