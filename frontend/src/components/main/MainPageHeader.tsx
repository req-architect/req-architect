import {
    TextField,
    Button,
    Typography,
    AppBar,
    Toolbar,
    Box,
} from "@mui/material";

import { useNavigate } from "react-router-dom";
import { useState } from "react";


export default function MainPageHeader() {
    const navigate = useNavigate();
    const [commitTextFieldValue, setcommitTextFieldValue] = useState('');

    const handleLogOut = () => {
        navigate("/");
    };

    const changeCommitFieldValue = (event: React.ChangeEvent<HTMLInputElement>) => {
        setcommitTextFieldValue(event.target.value);
    }
    
    const handleCommit = () => {
        console.log('Text from TextField:', commitTextFieldValue);
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
                <Typography
                    variant="h5"
                    color="black"
                    component="div"
                    sx={{ minWidth: "fit-content", mr: 2 }}
                >
                    PZSP2-KUKIWAKO
                </Typography>
                <Box
                    display="flex"
                    justifyContent="center"
                    alignItems="center"
                    sx={{ flexGrow: 1 }}
                >
                    <TextField
                        id="outlined-basic"
                        label="Comment"
                        multiline
                        variant="outlined"
                        maxRows={1}
                        sx={{ width: "50%", mr: 2, bgcolor: "white" }}
                        value={commitTextFieldValue}
                        onChange={changeCommitFieldValue}
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
                <Button
                    color="inherit"
                    sx={{
                        border: "1px solid green",
                        color: "green",
                        minWidth: "150px",
                        height: "40px",
                        mr: 2,
                    }}
                    onClick={handleLogOut}
                >
                    Log out
                </Button>
            </Toolbar>
        </AppBar>
    );
}
