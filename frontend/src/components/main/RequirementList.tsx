import { ReqDocument, Requirement } from "../../types.ts";
import { useEffect } from "react";
import { List, Box, TextField, Typography, Button } from "@mui/material";

const ButtonStyle = {
    background: "green",
    color: "white",
    minWidth: "80px",
    height: "40px",
    mt: 2,
    "&:hover": {
        background: "#689F38",
    },
};

export default function RequirementList() {
    return (
        <List sx={{ overflow: "auto", maxHeight: "91vh" }}>
            <Box>
                <Typography variant="h6" color="black" sx={{ mt: 10 }}>
                    Requirement 1
                </Typography>
                <TextField
                    multiline
                    rows={4}
                    defaultValue="Lorem ipsum ipsum lorem"
                    sx={{ width: "100%", mt: 2 }}
                />
                <Button size="large" sx={ButtonStyle}>
                    Ok
                </Button>
            </Box>
            <Box>
                <Typography variant="h6" color="black" sx={{ mt: 10 }}>
                    Requirement 2
                </Typography>
                <TextField
                    multiline
                    rows={4}
                    defaultValue="Lorem ipsum ipsum lorem"
                    sx={{ width: "100%", mt: 2 }}
                />
                <Button size="large" sx={ButtonStyle}>
                    Ok
                </Button>
            </Box>
            <Box>
                <Typography variant="h6" color="black" sx={{ mt: 10 }}>
                    Requirement 3
                </Typography>
                <TextField
                    multiline
                    rows={4}
                    defaultValue="Lorem ipsum ipsum lorem"
                    sx={{ width: "100%", mt: 2 }}
                />
                <Button size="large" sx={ButtonStyle}>
                    Ok
                </Button>
            </Box>
            <Box>
                <Typography variant="h6" color="black" sx={{ mt: 10 }}>
                    Requirement 4
                </Typography>
                <TextField
                    multiline
                    rows={4}
                    defaultValue="Lorem ipsum ipsum lorem"
                    sx={{ width: "100%", mt: 2 }}
                />
                <Button size="large" sx={ButtonStyle}>
                    Ok
                </Button>
            </Box>
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
