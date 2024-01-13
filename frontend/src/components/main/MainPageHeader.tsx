import {
    TextField,
    Button,
    Typography,
    AppBar,
    Toolbar,
    Box,
} from "@mui/material";

import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { postCommit } from "../../lib/api/gitService";
import { toast } from "react-toastify";
import { setLocalStorageObject } from "../../lib/localStorageUtil";

export default function MainPageHeader() {
    const navigate = useNavigate();
    const [commitTextFieldValue, setcommitTextFieldValue] = useState("");
    const [errorState, setErrorState] = useState<string | null>(null);

    const handleLogOut = () => {
        setLocalStorageObject("chosenRepositoryName", null);
        setLocalStorageObject("jwtToken", null);
        navigate("/");
    };

    const changeCommitFieldValue = (
        event: React.ChangeEvent<HTMLInputElement>,
    ) => {
        setcommitTextFieldValue(event.target.value);
    };

    const handleCommit = async () => {
        if (!commitTextFieldValue) {
            setErrorState("Commit message cannot be empty");
            return;
        }
        if (errorState) setErrorState(null);
        const response = await postCommit(commitTextFieldValue);
        response.message;
        if (response.message.includes("Success")) {
            toast.success("Changes pushed");
            setcommitTextFieldValue("");
        }
    };

    return (
        <AppBar
            position="static"
            sx={{
                backgroundColor: "#EEEEEE",
                border: "1px solid green",
                boxShadow: "none",
                justifyContent: "center",
            }}
        >
            <Toolbar>
                <Typography
                    variant="h5"
                    color="black"
                    component="div"
                    sx={{ minWidth: "fit-content", mr: 2 }}
                >
                    PZSP2-KUKIWAKO
                </Typography>
                <Box
                    display="flex"
                    justifyContent="center"
                    alignItems="center"
                    sx={{ flexGrow: 1 }}
                >
                    <TextField
                        id="outlined-basic"
                        label={errorState ? errorState : "Comment"}
                        multiline
                        variant="outlined"
                        maxRows={1}
                        sx={{ width: "50%", mr: 2, bgcolor: "white" }}
                        value={commitTextFieldValue}
                        onChange={changeCommitFieldValue}
                        error={!!errorState}
                    ></TextField>
                    <Button
                        sx={{
                            background: "green",
                            color: "white",
                            minWidth: "80px",
                            height: "40px",
                            mr: 2,
                            "&:hover": {
                                background: "#689F38",
                            },
                        }}
                        onClick={handleCommit}
                    >
                        SAVE
                    </Button>
                </Box>
                <Button
                    color="inherit"
                    sx={{
                        border: "1px solid green",
                        color: "green",
                        minWidth: "150px",
                        height: "40px",
                        mr: 2,
                    }}
                    onClick={handleLogOut}
                >
                    Log out
                </Button>
            </Toolbar>
        </AppBar>
    );
}
