import { Fab, Grid } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";

export default function AddRequirement() {
    return (
        <Grid item justifyContent={"flex-end"} sx={{ alignSelf: "flex-end" }}>
            <Fab
                size="small"
                color="success"
                aria-label="add"
                sx={{ mt: 2, ml: "auto", mr: 8, mb: 2 }}
            >
                <AddIcon />
            </Fab>
        </Grid>
    );
}
