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
import { useEffect, useState } from "react";
import { postDocument } from "../../lib/api/documentService.ts";

export default function AddDocument({
    mode,
    setMode,
    prefixes,
    onAddDocument,
}: {
    mode: string;
    setMode: (mode: string) => void;
    prefixes: string[];
    onAddDocument: () => void;
}) {
    const [formData, setFormData] = useState({
        text: "",
        selectedOption: "",
    });

    useEffect(() => {
        if (formData.selectedOption === "" && prefixes.length > 0) {
            setFormData((prev) => ({
                ...prev,
                selectedOption: prefixes[0],
            }));
        }
    }, [formData.selectedOption, prefixes]);

    const handleClick = () => {
        setMode("select");
    };

    const handleAddDocument = async (event: { preventDefault: () => void }) => {
        event.preventDefault(); //prevent: localhost/:1 Form submission canceled because the form is not connected
        if (!formData.text) {
            alert("Please enter a document prefix");
            return;
        }
        if (formData.selectedOption === "") {
            console.log("No parent prefix selected");
            await postDocument(formData.text);
        } else {
            console.log("Parent prefix selected:", formData.selectedOption);
            await postDocument(formData.text, formData.selectedOption);
        }
        setMode("add");
        onAddDocument();
    };

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
                                    options={prefixes}
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
