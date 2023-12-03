import { useNavigate } from "react-router-dom";
import Grid from "@mui/material/Grid";
import RepoList from "../components/choosing-repo/RepoList.tsx";
import Button from "@mui/material/Button";
import { Typography } from "@mui/material";

export default function ChoosingRepoPage() {
  const navigate = useNavigate();

  const handleLoginButtonClick = () => {
    // Perform login logic if needed
    // Then, navigate to the MainPage
    navigate("/main");
  };
  return (
    <>
      <Grid
        container
        direction={"column"}
        sx={{
          height: "65vh",
          width: "30%",
          backgroundColor: "#eeeeee",
          justifyContent: "space-between",
          allignSelf: "center",
          margin: "auto",
          marginTop: "10%",
          alignItems: "center",
          p: 8,
        }}
      >
        <Typography variant="h3" color="black" align="center">
          Choose your Repository
        </Typography>
        <RepoList />
        <Button
          size="large"
          variant="contained"
          color="success"
          onClick={handleLoginButtonClick}
          sx={{ mb: 10 }}
        >
          CHOOSE
        </Button>
      </Grid>
    </>
  );
}
