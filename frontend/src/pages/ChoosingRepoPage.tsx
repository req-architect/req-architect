import { useNavigate } from "react-router-dom";
import RepoList from "../components/choosing-repo/RepoList.tsx";
import Button from "@mui/material/Button";
import { Typography } from "@mui/material";
import { Box } from "@mui/system";
import { useState } from "react";
import { postRepo } from "../lib/api/gitService.ts";
import { setLocalStorageObject } from "../lib/localStorageUtil.ts";
import { auto } from "@popperjs/core";
import CircularProgress from "@mui/material/CircularProgress";
import useLoginRedirect from "../hooks/useLoginRedirect.ts";
import { useAuth } from "../hooks/useAuthContext.ts";

export default function ChoosingRepoPage() {
    const navigate = useNavigate();
    const authTools = useAuth();
    const [chosenRepository, setChosenRepository] = useState<string>();
    const [mode, setMode] = useState<1 | 2>(1);
    useLoginRedirect(false, "/login");

    const handleRepoSelected = (repo: string) => {
        setChosenRepository(repo);
    };

    const handleLoginButtonClick = async () => {
        if (!chosenRepository) {
            return;
        }
        setLocalStorageObject("chosenRepositoryName", chosenRepository);
        setMode(2);
        await postRepo();
        navigate("/");
    };

    const handleLogOut = () => {
        setLocalStorageObject("chosenRepositoryName", null);
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
                    sx={{
                        display: "flex",
                        justifyContent: "flex-end",
                        pr: 2,
                    }}
                >
                    <Button
                        color="inherit"
                        sx={{
                            border: "1px solid green",
                            color: "green",
                            minWidth: "150px",
                            height: "40px",
                            mt: 2,
                        }}
                        onClick={handleLogOut}
                    >
                        Log out
                    </Button>
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
                    <RepoList onRepoSelected={handleRepoSelected} />
                    {mode === 1 ? (
                        <Button
                            size="large"
                            variant="contained"
                            color="success"
                            onClick={handleLoginButtonClick}
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
