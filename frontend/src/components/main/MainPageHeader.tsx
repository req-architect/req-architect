import {TextField, Button, Typography, AppBar, Toolbar, Box} from "@mui/material"


export default function MainPageHeader() {
  return (
    <AppBar
      position="static"
      sx={{ backgroundColor: '#EEEEEE', border: '1px solid green', boxShadow: 'none', justifyContent: "center"}}>
      <Toolbar>
        <Typography
          variant="h5"
          color="black"
          component="div"
          sx={{minWidth: 'fit-content', mr: 2}}>
          PZSP2-KUKIWAKO
        </Typography>
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          sx={{flexGrow: 1}}>
            <TextField
              id="outlined-basic"
              label="Comment"
              multiline
              variant="outlined"
              maxRows={1}
              sx={{ width: "50%", mr: 2, bgcolor: "white"}}>
            </TextField>
            <Button
              size="large"
              sx={{ background: 'green', color: 'white', minWidth: "80px", height: "40px" , mr: 2}}>
              SAVE
            </Button>
        </Box>
        <Button
          color="inherit"
          sx={{ border: '1px solid green', color: 'green', minWidth: "150px", height: "40px" , mr: 2}}>
          Log out
        </Button>
      </Toolbar>
    </AppBar>
  );
}
