import {
    TextField,
    Button,
    Typography,
    AppBar,
    Toolbar,
    Box,
} from "@mui/material";

import { useState } from "react";
import { postCommit } from "../../lib/api/gitService";
import { toast } from "react-toastify";
import { useAuth } from "../../hooks/useAuthContext.ts";
import useRepoContext from "../../hooks/useRepoContext.ts";
import { APIError } from "../../lib/api/fetchAPI.ts";
import LogoutIcon from "@mui/icons-material/Logout";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import IconButton from "@mui/material/IconButton";
import { grey } from "@mui/material/colors";
import UndoIcon from "@mui/icons-material/Undo";

/*
    This component is the header of the main page.
    It will display the name of the repository and a text field to add a commit message.
    It will also display a logout button.
*/

export default function MainPageHeader() {
    const [commitTextFieldValue, setcommitTextFieldValue] = useState("");
    const [errorState, setErrorState] = useState<string | null>(null);
    const authTools = useAuth();
    const repoTools = useRepoContext();

    const handleLogOut = () => {
        repoTools.setRepositoryName(null);
        authTools.logout();
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
        if (!authTools.tokenStr || !repoTools.repositoryName) {
            return;
        }
        if (errorState) setErrorState(null);
        await postCommit(
            authTools.tokenStr,
            repoTools.repositoryName,
            commitTextFieldValue,
        )
            .then(() => {
                toast.success("Changes pushed");
                setcommitTextFieldValue("");
            })
            .catch((e) => {
                if (e instanceof APIError) {
                    if (e.api_error_code == "INVALID_TOKEN") {
                        authTools.logout(e.message);
                        return;
                    }
                    toast.error(e.message);
                    return;
                }
                toast.error(
                    `An error occurred while trying to save changes: ${e.name}`,
                );
                console.error(e);
            });
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
                <Box sx={{ display: "flex", gap: "5px" }}>
                    <IconButton
                        onClick={() => {
                            repoTools.setRepositoryName(null);
                        }}
                    >
                        <UndoIcon sx={{ color: grey[800] }} />
                    </IconButton>
                    <Box sx={{ display: "flex", alignItems: "center" }}>
                        <Typography
                            variant="h5"
                            color="black"
                            component="div"
                            sx={{ minWidth: "fit-content", mr: 2 }}
                        >
                            {repoTools.repositoryName}
                        </Typography>
                    </Box>
                </Box>
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
                <Box display="flex" justifyContent="center" gap="1vh">
                    <AccountCircleIcon
                        sx={{ color: grey[600] }}
                        fontSize="large"
                    />
                    <Box sx={{ display: "flex", alignItems: "center" }}>
                        <Typography
                            variant="h5"
                            color="black"
                            component="div"
                            sx={{ minWidth: "fit-content", mr: 2 }}
                        >
                            {authTools.user?.login}
                        </Typography>
                    </Box>
                    <IconButton>
                        <LogoutIcon
                            sx={{ color: grey[900] }}
                            onClick={handleLogOut}
                        />
                    </IconButton>
                </Box>
            </Toolbar>
        </AppBar>
    );
}
