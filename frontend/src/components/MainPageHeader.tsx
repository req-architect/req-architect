import {TextField, Button, Typography, AppBar, Toolbar, Box} from "@mui/material"


export default function MainPageHeader() {
  return (
    <AppBar
      position="static"
      sx={{ backgroundColor: '#EEEEEE', border: '1px solid green', boxShadow: 'none' }}>
      <Toolbar>
        <Typography
          variant="h5"
          color="black"
          component="div"
          sx={{minWidth: "300px"}}>
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
            sx={{ width: "50%", mr: 2, bgcolor: "white", marginRight: 20}}>
        </TextField>
        </Box>
        <Button
          color="inherit"
          size="large"
          sx={{ border: '1px solid green', color: 'green'}}>
          Log out
        </Button>
      </Toolbar>
    </AppBar>
  );
}

// export default function MainPageHeader() {
//   return (
//     <Grid
//       container
//       sx={{
//         height: "10vh",
//         minWidth: 1025,
//         visibility: "hidden",
//       }}
//     >
//       <Grid
//         container
//         p={2}
//         direction={"row"}
//         justifyContent={"space-between"}
//         alignItems="center"
//         borderBottom="1px solid green"
//         sx={{ visibility: "visible" }}
//         bgcolor={"#EEEEEE"}
//       >
//         <Typography variant="h5" color="black">
//           PZSP2-KUKIWAKO
//         </Typography>

//         <Grid
//           container
//           width="fit-content"
//           height="fit-content"
//           alignItems="center"
//         >
          // <TextField
          //   id="outlined-basic"
          //   label="Comment"
          //   multiline
          //   variant="outlined"
          //   maxRows={1}
          //   sx={{ width: "50vh", mr: 2, bgcolor: "white" }}
          // />
//           <Button
//             size="medium"
//             variant="contained"
//             color="success"
//             sx={{ height: "50%" }}
//           >
//             SAVE
//           </Button>
//         </Grid>

//         <Button
//           size="medium"
//           variant="outlined"
//           color="success"
//           sx={{ height: "50%" }}
//         >
//           LOG OUT
//         </Button>
//       </Grid>
//     </Grid>
//   );
// }
