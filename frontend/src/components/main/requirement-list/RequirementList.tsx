import { Requirement } from "../../../types.ts";
import RequirementComponent from "./RequirementComponent.tsx";
import { List, Box, Typography } from "@mui/material";
import { createContext } from "react";
import { RequirementContextType } from "../../../hooks/useRequirementContext.ts";

/* 
    This component is used to display a list of requirements.
    It will display the requirements in a list.
*/

export const RequirementContext = createContext<RequirementContextType | null>(
    null,
);

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
                    key={requirement.id}
                    sx={{
                        display: "flex",
                        justifyContent: "center",
                        ml: 2,
                        mr: 2,
                    }}
                >
                    <RequirementContext.Provider
                        value={{ requirement, refreshRequirements }}
                    >
                        <RequirementComponent />
                    </RequirementContext.Provider>
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
