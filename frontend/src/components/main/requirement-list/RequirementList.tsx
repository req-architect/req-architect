import { Requirement } from "../../../types.ts";
import RequirementComponent from "./RequirementComponent.tsx";
import { List, Box, Typography } from "@mui/material";

export default function RequirementList({
    requirements,
    refreshRequirements,
}: {
    requirements: Requirement[];
    refreshRequirements: () => void;
}) {
    return requirements.length > 0 ? (
        <List>
            {requirements.map((requirement) => (
                <Box
                    sx={{
                        display: "flex",
                        justifyContent: "center",
                        ml: 2,
                        mr: 2,
                    }}
                >
                    <RequirementComponent
                        requirement={requirement}
                        refreshRequirements={refreshRequirements}
                    />
                </Box>
            ))}
        </List>
    ) : (
        <Typography
            sx={{
                fontSize: 24,
                textAlign: "center",
                fontWeight: "bold",
                mt: 2,
            }}
        >
            No requirement in this document yet
        </Typography>
    );
}
