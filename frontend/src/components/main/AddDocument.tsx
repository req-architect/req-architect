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
import { useEffect, useMemo, useState } from "react";
import { postDocument } from "../../lib/api/documentService.ts";
import { ReqDocumentWithChildren } from "../../types.ts";
import { useAuth } from "../../hooks/useAuthContext.ts";
import useRepoContext from "../../hooks/useRepoContext.ts";
import { APIError } from "../../lib/api/fetchAPI.ts";
import { toast } from "react-toastify";

/*
    This component allows the user to add a document.
    It will display a text field for the document prefix and a dropdown to select the parent document.
*/

type AddDocumentMode = "add" | "select";

function extractPrefixes(document: ReqDocumentWithChildren) {
    let prefixes: string[] = [document.prefix];

    if (document.children && document.children.length > 0) {
        document.children.forEach((child) => {
            prefixes = [...prefixes, ...extractPrefixes(child)];
        });
    }
    return prefixes;
}

type ErrorState = {
    prefixError: string | null;
    parentPrefixError: string | null;
};

export default function AddDocument({
    rootDocument,
    refreshDocuments,
}: {
    rootDocument: ReqDocumentWithChildren | null;
    refreshDocuments: () => void;
}) {
    const authTools = useAuth();
    const repoTools = useRepoContext();
    const [mode, setMode] = useState<AddDocumentMode>("add");
    const [formData, setFormData] = useState<{
        text: string;
        selectedOption: string | null;
    }>({
        text: "",
        selectedOption: null,
    });
    const [errorState, setErrorState] = useState<ErrorState>({
        prefixError: null,
        parentPrefixError: null,
    });

    const prefixes = useMemo(
        () => (rootDocument ? extractPrefixes(rootDocument) : []),
        [rootDocument],
    );

    useEffect(() => {
        setFormData({
            text: "",
            selectedOption: prefixes.length > 0 ? prefixes[0] : null,
        });
    }, [prefixes]);

    const handleAddDocument = async (event: { preventDefault: () => void }) => {
        event.preventDefault(); //prevent: localhost/:1 Form submission canceled because the form is not connected
        if (!authTools.tokenStr || !repoTools.repositoryName) {
            return;
        }
        let newErrorState: ErrorState = {
            prefixError: null,
            parentPrefixError: null,
        };
        if (!formData.text) {
            newErrorState = {
                ...newErrorState,
                prefixError: "Document prefix cannot be empty",
            };
        }
        if (formData.text && prefixes.includes(formData.text)) {
            newErrorState = {
                ...newErrorState,
                prefixError: "Document prefix must be unique",
            };
        }
        if (formData.selectedOption === null && prefixes.length > 0) {
            newErrorState = {
                ...newErrorState,
                parentPrefixError: "Parent prefix cannot be empty",
            };
        }
        if (
            newErrorState.prefixError !== null ||
            newErrorState.parentPrefixError !== null
        ) {
            setErrorState(newErrorState);
            return;
        }
        setErrorState(newErrorState);
        let docPromise: Promise<void>;
        if (formData.selectedOption === null) {
            docPromise = postDocument(
                authTools.tokenStr,
                repoTools.repositoryName,
                formData.text,
            );
        } else {
            docPromise = postDocument(
                authTools.tokenStr,
                repoTools.repositoryName,
                formData.text,
                formData.selectedOption,
            );
        }
        await docPromise.then(refreshDocuments).catch((e) => {
            if (e instanceof APIError) {
                if (e.api_error_code == "INVALID_TOKEN") {
                    authTools.logout(e.message);
                    return;
                }
                toast.error(e.message);
                return;
            }
            toast.error(
                `An error occurred while trying to add document: ${e.name}`,
            );
            console.error(e);
        });
    };

    return (
        <Box
            alignItems="stretch"
            sx={{
                alignSelf: "flex-end",
                marginTop: "auto",
                ml: 2,
                mr: 2,
                mb: 2,
                justifyContent: "flex-end",
            }}
        >
            {mode === "add" ? (
                <Fab
                    size="small"
                    color="success"
                    aria-label="add"
                    sx={{}}
                    onClick={() => {
                        setMode("select");
                    }}
                >
                    <AddIcon />
                </Fab>
            ) : (
                <Box>
                    <form>
                        <TextField
                            label="New document prefix"
                            fullWidth
                            sx={{ mt: 2, mb: 2 }}
                            value={formData.text}
                            onChange={(event) => {
                                setFormData((prev) => ({
                                    ...prev,
                                    text: event.target.value,
                                }));
                            }}
                            error={!!errorState.prefixError}
                            helperText={errorState.prefixError}
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
                                        selectedOption: newValue || null,
                                    }));
                                }}
                                renderInput={(params) => (
                                    <TextField
                                        {...params}
                                        label="Parent prefix"
                                        error={!!errorState.parentPrefixError}
                                        helperText={
                                            errorState.parentPrefixError
                                        }
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
                    </form>
                    <Box sx={{ mb: 2 }}>
                        <Button
                            type="submit"
                            variant="contained"
                            color="success"
                            onClick={handleAddDocument}
                            sx={{ width: "100%" }}
                        >
                            Add Document
                        </Button>
                    </Box>
                    <Box sx={{}}>
                        <Button
                            variant="contained"
                            color="success"
                            onClick={() => {
                                setMode("add");
                            }}
                            sx={{ width: "100%" }}
                        >
                            Back
                        </Button>
                    </Box>
                </Box>
            )}
        </Box>
    );
}
