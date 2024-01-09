import { Button, Typography } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";
import { Box } from "@mui/system";
import { auto } from "@popperjs/core";

export default function LoginPage() {
    const handleGithubClick = () => {
        window.location.href =
            import.meta.env.VITE_APP_API_URL + "/MyServer/login/github";
    };
    const handleGitLabClick = () => {
        window.location.href =
            import.meta.env.VITE_APP_API_URL + "/MyServer/login/gitlab";
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
    );
}
