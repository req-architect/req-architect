import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

export default function MainPageHeader() {
  return (
    <Grid
      container
      sx={{
        height: "10vh",
        minWidth: 1025,
        visibility: "hidden",
      }}
    >
      <Grid
        container
        p={2}
        direction={"row"}
        justifyContent={"space-between"}
        alignItems="center"
        borderBottom="1px solid green"
        sx={{ visibility: "visible" }}
        bgcolor={"#EEEEEE"}
      >
        <Typography variant="h5" color="black">
          PZSP2-KUKIWAKO
        </Typography>

        <Grid
          container
          width="fit-content"
          height="fit-content"
          alignItems="center"
        >
          <TextField
            id="outlined-basic"
            label="Comment"
            multiline
            variant="outlined"
            maxRows={1}
            sx={{ width: "50vh", mr: 2, bgcolor: "white" }}
          />
          <Button
            size="medium"
            variant="contained"
            color="success"
            sx={{ height: "50%" }}
          >
            SAVE
          </Button>
        </Grid>

        <Button
          size="medium"
          variant="outlined"
          color="success"
          sx={{ height: "50%" }}
        >
          LOG OUT
        </Button>
      </Grid>
    </Grid>
  );
}
