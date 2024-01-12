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

export default function ChoosingRepoPage() {
    const navigate = useNavigate();
    const [chosenRepository, setChosenRepository] = useState<string>();
    const [mode, setMode] = useState<1 | 2>(1);

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
        navigate("/main_page");
    };
    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                minHeight: "100vh",
            }}
        >
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
                    <CircularProgress sx={{ alignSelf: "center", mb: 10 }} />
                )}
            </Box>
        </Box>
    );
}
