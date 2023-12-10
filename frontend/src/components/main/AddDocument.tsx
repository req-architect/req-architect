import {
    Autocomplete,
    Button,
    Fab,
    FormControl,
    Box,
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
        if (/^\d+$/.test(formData.text.charAt(formData.text.length - 1))) { // if is digit
            alert("Document prefix cannot end with a digit");
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
        <Box
            alignItems="stretch"
            sx={{ alignSelf: "flex-end", marginTop: "auto", ml: 2, mr: 2, mb: 2, justifyContent: "flex-end"}}
        >
            {mode === "add" ? (
                <Fab
                    size="small"
                    color="success"
                    aria-label="add"
                    sx={{  }}
                    onClick={handleClick}
                >
                    <AddIcon />
                </Fab>
            ) : (
                <form onSubmit={handleAddDocument}>
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
                    <Button
                        type="submit"
                        variant="contained"
                        color="success"
                    >
                        Add Document
                    </Button>
                </form>
            )}
        </Box>
    );
}
