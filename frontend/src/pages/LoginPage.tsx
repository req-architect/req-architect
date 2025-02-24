import { Button, Typography } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";
import { Box } from "@mui/system";
import { auto } from "@popperjs/core";
import useLoginRedirect from "../hooks/useLoginRedirect.ts";
import { useAuth } from "../hooks/useAuthContext.ts";

/*
    This page is used to provide the user with options to login with GitHub or GitLab.
    It will redirect the user to GitLab or GitHub to login and authorization page.
*/

export default function LoginPage() {
    useLoginRedirect(true, "/repo");
    const authTools = useAuth();
    const handleGithubClick = () => {
        window.location.href =
            import.meta.env.VITE_APP_API_URL + "/api/login/github";
    };
    const handleGitLabClick = () => {
        window.location.href =
            import.meta.env.VITE_APP_API_URL + "/api/login/gitlab";
    };

    return (
        !authTools.initialLoading && (
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
                        Welcome
                    </Typography>
                    <Button
                        fullWidth
                        size="large"
                        variant="contained"
                        sx={{
                            backgroundColor: "#fc6d26", // GitLab color
                            color: "#ffffff",
                            "&:hover": {
                                backgroundColor: "#e24329",
                            },
                            width: "80%",
                            mt: auto,
                            mb: 2,
                            alignSelf: "center",
                        }}
                        onClick={handleGitLabClick}
                    >
                        <img
                            src="/icons/gitlab.svg"
                            alt="GitLab Icon"
                            style={{ marginRight: "8px" }}
                        />
                        Login with GitLab
                    </Button>
                    <Button
                        fullWidth
                        size="large"
                        variant="contained"
                        sx={{
                            backgroundColor: "#24292e", // GitHub color
                            color: "#ffffff",
                            "&:hover": {
                                backgroundColor: "#1c1f23",
                            },
                            width: "80%",
                            mb: 2,
                            alignSelf: "center",
                        }}
                        startIcon={<GitHubIcon />}
                        onClick={handleGithubClick}
                    >
                        Login with GitHub
                    </Button>
                </Box>
            </Box>
        )
    );
}
