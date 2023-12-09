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
import {PostDocument} from "../../hooks/MainFunctions.ts"
import { RenderTree } from "./DocumentList.tsx";


interface DocumentListProps {
    documents: RenderTree; // Pass the documents as a prop
}

export default function AddDocument({
    mode,
    setMode,
    prefixes,
}: {
    mode: string;
    setMode: (mode: string) => void;
    prefixes: string[];
}) {
    const uniqueOptions = Array.from(new Set(prefixes)).sort((a, b) => a.localeCompare(b));
    
    const [formData, setFormData] = useState({
        text: "",
        selectedOption: "",
    });
    
    useEffect(() => {
        if (formData.selectedOption === "" && uniqueOptions.length > 0) {
            setFormData((prev) => ({
                ...prev,
                selectedOption: uniqueOptions[0],
            }));
        }
    }, [formData.selectedOption, uniqueOptions]);
    

    const handleClick = () => {
        setMode("select");
    };
    
    const handleAddDocument = (event: { preventDefault: () => void }) => {
        event.preventDefault(); //prevent: localhost/:1 Form submission canceled because the form is not connected
        if (!formData.text) {
            alert("Please enter a document prefix");
            return;
        }
        if (formData.selectedOption === "") {
            console.log("No parent prefix selected");
            PostDocument(formData.text);
        }
        else{
            console.log("Parent prefix selected:", formData.selectedOption);
        PostDocument(formData.text, formData.selectedOption);}
        setMode("add");
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
                                    options={uniqueOptions}
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
