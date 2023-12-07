import {
    Autocomplete,
    Button,
    Fab,
    FormControl,
    Grid,
    Paper,
    TextField,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { useState } from "react";

export default function AddDocument({
    mode,
    setMode,
}: {
    mode: string;
    setMode: (mode: string) => void;
}) {
    const [formData, setFormData] = useState({
        text: "",
        selectedOption: "",
    });

    const handleClick = () => {
        setMode("select");
    };

    const handleAddDocument = (event: { preventDefault: () => void }) => {
        event.preventDefault(); //prevent: localhost/:1 Form submission canceled because the form is not connected
        //logika dodawania dokumentu
        console.log("Sending data:", formData);
        setMode("add");
    };

    const options = ["Option 1", "Option 2", "Option 3", "root", "1", "srd"];

    return (
        <Grid
            container
            direction="column"
            alignItems="stretch"
            sx={{ alignSelf: "flex-end", marginTop: "auto", mb: 2 }}
        >
            {mode === "add" ? (
                <Grid
                    item
                    container
                    justifyContent={"flex-end"}
                    mt={2}
                    height={"10vh"}
                >
                    <Fab
                        size="small"
                        color="success"
                        aria-label="add"
                        sx={{ ml: "auto", mr: 8, mb: 2 }}
                        onClick={handleClick}
                    >
                        <AddIcon />
                    </Fab>
                </Grid>
            ) : (
                <form onSubmit={handleAddDocument}>
                    <Grid
                        container
                        direction="column"
                        justifyContent="flex-start"
                        alignItems="stretch"
                        height={"35vh"}
                        minHeight={250}
                        overflow={"hidden"}
                        paddingLeft={2}
                        paddingRight={2}
                    >
                        <Grid item>
                            <TextField
                                label="New document prefix"
                                fullWidth
                                sx={{ mt: 2, mb: 2 }}
                                onChange={(event) => {
                                    setFormData((prev) => ({
                                        ...prev,
                                        text: event.target.value,
                                    }));
                                }}
                            />
                        </Grid>
                        <Grid item>
                            <FormControl
                                fullWidth
                                variant="outlined"
                                sx={{ mt: 2, mb: 2 }}
                            >
                                <Autocomplete
                                    value={formData.selectedOption}
                                    onChange={(_event, newValue) => {
                                        setFormData((prev) => ({
                                            ...prev,
                                            selectedOption: newValue || "",
                                        }));
                                    }}
                                    renderInput={(params) => (
                                        <TextField
                                            {...params}
                                            label="Parent prefix"
                                        />
                                    )}
                                    PaperComponent={({ children }) => (
                                        <Paper
                                            style={{
                                                maxHeight: "150px",
                                                overflowY: "auto",
                                            }}
                                        >
                                            {children}
                                        </Paper>
                                    )}
                                    options={options.sort(
                                        (a, b) => -b[0].localeCompare(a[0]),
                                    )}
                                />
                            </FormControl>
                        </Grid>
                        <Grid item>
                            <Button
                                type="submit"
                                variant="contained"
                                color="success"
                            >
                                Add Document
                            </Button>
                        </Grid>
                    </Grid>
                </form>
            )}
        </Grid>
    );
}
