import MainPageHeader from "../components/main/MainPageHeader.tsx";
import DocumentList from "../components/main/DocumentList.tsx";
import RequirementList from "../components/main/RequirementList.tsx";
import RequirementDetails from "../components/main/RequirementDetails.tsx";
import { useState } from "react";
import { ReqDocument, Requirement } from "../types.ts";
import Grid from "@mui/material/Grid";
import AddRequirement from "../components/main/AddRequirement.tsx";
import Metadata from "../components/main/Metadata.tsx";
import TextField from "@mui/material/TextField";
import { Box, Container } from "@mui/material";
import { Typography } from "@mui/material";

export default function MainPage() {
    const [selectedDocReq, setSelectedDocReq] = useState<
        [ReqDocument | null, Requirement | null]
    >([null, null]);

    function updateDocument(document: ReqDocument) {
        setSelectedDocReq([document, null]);
    }

    function updateRequirement(requirement: Requirement) {
        setSelectedDocReq((prev) => [prev[0], requirement]);
    }

    // "100%"
    return (
        <div
            style={{
                width: "100%",
                minWidth: "120vh",
                height: "100vh",
                display: "flex",
                flexDirection: "column",
            }}
        >
            <MainPageHeader />
            <Grid
                container
                justifyContent={"space-between"}
                sx={{ borderBottom: "0.5px solid green", overflow: "hidden" }}
            >
                <Grid item xs={3} display={"flex"} flexDirection={"column"}>
                    <DocumentList updateDocument={updateDocument} />
                    <AddRequirement />
                </Grid>
                <Grid item xs={6} sx={{ height: "100%", overflow: "auto" }}>
                    <RequirementList />
                </Grid>
                <Grid item xs={0} />
                <Grid item xs={2}>
                    <Metadata />
                </Grid>
            </Grid>
        </div>
    );
}

{
    /* <>
      <MainPageHeader />
      <Grid container visibility={"hidden"} m={0}>
        <Grid
          container
          sx={{
            height: "90vh",
            minWidth: 1025,
            visibility: "visible",
            justifyContent: "space-between",
          }}
        >
          <Grid
            sx={{
              borderRight: "1px solid green",
              minWidth: "fill-content",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <DocumentList updateDocument={updateDocument} />
            <AddRequirement />
          </Grid>

          <Grid
            container
            direction={"column"}
            sx={{ p: 0, width: "50%", allignContent: "center" }}
          >
            <RequirementList
              document={selectedDocReq[0]}
              updateRequirement={updateRequirement}
            />
            <RequirementDetails requirement={selectedDocReq[1]} />
          </Grid>

          <Metadata />
        </Grid>
      </Grid>
    </> */
}
