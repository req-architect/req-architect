import { useNavigate } from "react-router-dom";
import RepoList from "../components/choosing-repo/RepoList.tsx";
import Button from "@mui/material/Button";
import { Typography } from "@mui/material";
import { Box } from "@mui/system";
import { useState } from "react";
import { postRepo } from "../lib/api/gitService.ts";
import { auto } from "@popperjs/core";
import CircularProgress from "@mui/material/CircularProgress";
import useLoginRedirect from "../hooks/useLoginRedirect.ts";
import { useAuth } from "../hooks/useAuthContext.ts";
import useRepoContext from "../hooks/useRepoContext.ts";
import { APIError } from "../lib/api/fetchAPI.ts";
import { toast } from "react-toastify";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import { grey } from "@mui/material/colors";
import IconButton from "@mui/material/IconButton";
import LogoutIcon from "@mui/icons-material/Logout";

/*
    This page is used to provide the user with a list of repositories to choose from.
    It will then store the chosen repository in the repo context and redirect the user to the main page.
*/

export default function ChoosingRepoPage() {
    const navigate = useNavigate();
    const authTools = useAuth();
    const [chosenRepository, setChosenRepository] = useState<string | null>(
        null,
    );
    const [mode, setMode] = useState<1 | 2>(1);
    const repoContext = useRepoContext();
    useLoginRedirect(false, "/login");

    const handleChooseRepo = async () => {
        if (!chosenRepository || !authTools.tokenStr) {
            return;
        }

        setMode(2);
        await postRepo(authTools.tokenStr, chosenRepository)
            .then(() => {
                repoContext.setRepositoryName(chosenRepository);
                navigate("/");
            })
            .catch((e) => {
                setMode(1);
                if (e instanceof APIError) {
                    if (e.api_error_code == "INVALID_TOKEN") {
                        authTools.logout(e.message);
                        return;
                    }
                    toast.error(e.message);
                    return;
                }
                toast.error(
                    `An error occurred while trying to choose repo: ${e.name}`,
                );
                console.error(e);
            });
    };

    const handleLogOut = () => {
        authTools.logout();
    };

    return (
        !authTools.initialLoading && (
            <Box
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    minHeight: "100vh",
                }}
            >
                <Box
                    display="flex"
                    justifyContent="flex-end"
                    alignItems="center"
                    gap="1vh"
                    paddingRight="5vh"
                    paddingTop="1.5vh"
                >
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
                <Box
                    sx={{
                        minHeight: "450px",
                        minWidth: "450px",
                        backgroundColor: "#f5f5f5",
                        margin: "auto",
                        p: 8,
                        boxShadow: "0px 15px 12px -1px rgba(136, 136, 142, 1)",
                        overflow: auto,
                        display: "flex",
                        flexDirection: "column",
                        alignSelf: "center",
                    }}
                >
                    <Typography variant="h3" color="black" align="center">
                        Choose your Repository
                    </Typography>
                    <RepoList
                        chosenRepository={chosenRepository}
                        setChosenRepository={setChosenRepository}
                    />
                    {mode === 1 ? (
                        <Button
                            size="large"
                            variant="contained"
                            color="success"
                            onClick={handleChooseRepo}
                            sx={{ mb: 10, alignSelf: "center" }}
                        >
                            CHOOSE
                        </Button>
                    ) : (
                        <CircularProgress
                            sx={{ alignSelf: "center", mb: 10 }}
                        />
                    )}
                </Box>
            </Box>
        )
    );
}
