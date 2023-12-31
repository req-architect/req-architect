import { useContext } from "react";
import { MainContext } from "../../../pages/MainPage.tsx";
import { Box, List, ListItem, ListItemText, Typography } from "@mui/material";
import LinkIcon from "@mui/icons-material/Link";
import RequirementAddLink from "./RequirementAddLink.tsx";

export default function RequirementDetails() {
    const contextTools = useContext(MainContext);
    return (
        <Box
            borderLeft="1px solid green"
            sx={{
                p: 0,
                paddingLeft: 2,
                paddingTop: 2,
                // width: "15%",
                height: "100%",
            }}
        >
            {contextTools?.data.selectedRequirement && (
                <Box>
                    <Box textAlign="center">
                        <Typography variant="h5" fontWeight="bold" mb={1}>
                            {contextTools.data.selectedRequirement.id}
                        </Typography>
                        <Typography sx={{ mt: 1 }}>
                            Reviewed:{" "}
                            {contextTools?.data.selectedRequirement?.reviewed
                                ? "Yes"
                                : "No"}
                        </Typography>
                    </Box>
                    <Typography variant="h6" fontWeight="bold">
                        Links:
                    </Typography>
                    <Box>
                        {contextTools.data.selectedRequirement.links.length >
                        0 ? (
                            <List>
                                {contextTools.data.selectedRequirement.links.map(
                                    (linkText, index) => (
                                        <ListItem key={index}>
                                            <LinkIcon
                                                fontSize="small"
                                                sx={{ marginRight: 1 }}
                                            />
                                            <ListItemText primary={linkText} />
                                        </ListItem>
                                    ),
                                )}
                            </List>
                        ) : (
                            <Typography>No links</Typography>
                        )}
                    </Box>
                    <RequirementAddLink />
                </Box>
            )}
        </Box>
    );
}
