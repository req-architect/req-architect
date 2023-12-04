import MainPageHeader from "../components/main/MainPageHeader.tsx";
import DocumentList from "../components/main/DocumentList.tsx";
import RequirementList from "../components/main/RequirementList.tsx";
import RequirementDetails from "../components/main/RequirementDetails.tsx";
import {useState} from "react";
import {ReqDocument, Requirement} from "../types.ts";
import Grid from "@mui/material/Grid";
import AddRequirement from "../components/main/AddRequirement.tsx";
import Metadata from "../components/main/Metadata.tsx";

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
        <div style={{height: '100vh'}}>
            <MainPageHeader/>
            <Grid display="flex" height="100%" flexDirection="column">
                <Grid
                    container
                    sx={{
                        height: "100%",
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
                        <DocumentList updateDocument={updateDocument}/>
                        <AddRequirement/>
                    </Grid>

                    <Grid
                        container
                        direction={"column"}
                        sx={{p: 0, width: "50%", allignContent: "center"}}
                    >
                        <RequirementList
                            document={selectedDocReq[0]}
                            updateRequirement={updateRequirement}
                        />
                        <RequirementDetails requirement={selectedDocReq[1]}/>
                    </Grid>

                    <Metadata/>
                </Grid>
            </Grid>
        </div>
    );
}

{/* <>
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