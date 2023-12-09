import MainPageHeader from "../components/main/MainPageHeader.tsx";
import DocumentList from "../components/main/DocumentList.tsx";
import { createContext, useEffect, useState } from "react";
import Grid from "@mui/material/Grid";
import { Container } from "@mui/material";
import useMainContext, { MainContextTools } from "../hooks/useMainContext.ts";
import AddDocument from "../components/main/AddDocument.tsx";
import RequirementList from "../components/main/requirement-list/RequirementList.tsx";
import RequirementDetails from "../components/main/RequirementDetails.tsx";
import { RenderTree } from "../components/main/DocumentList.tsx";

export const MainContext = createContext<MainContextTools | null>(null);

export default function MainPage() {
    const mainContextTools = useMainContext();
    const [mode, setMode] = useState("add");
    const [fetchedDocuments, setFetchedDocuments] = useState<RenderTree>([]);
    const [fetchedPrefixes, setFetchedPrefixes] = useState<string[]>([]);
    
    
    const extractPrefixes = (document: { prefix: string; children?: any[] }) => {
        let prefixes: string[] = [document.prefix];
    
        if (document.children && document.children.length > 0) {
            document.children.forEach((child) => {
                prefixes = [...prefixes, ...extractPrefixes(child)];
            });
        }
    
        return prefixes;
    };
    
    useEffect(() => {
        // Fetch documents from Django backend
        fetch("http://localhost:8000/MyServer/doc/", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) =>  response.json())
          .then((data) => {
            // Set the fetched documents in state
            console.log("Fetched documents:", data);
            setFetchedDocuments(data);
            data.forEach((document: { prefix: string; children?: any[] | undefined; }) => {
                const documentPrefixes = extractPrefixes(document);
                setFetchedPrefixes((fetchedPrefixes) => [...fetchedPrefixes, ...documentPrefixes])});
          })
          .catch((error) => {
            if (error.message.includes("Internal Server Error")){
                console.log("Couldn't fetch documents:", error.message);
            }
            else if (error.message.includes("Unexpected token '<'")) {
                console.log("Empty document list");
            } 
            else {
            console.error("Error fetching documents:", error);}
            setFetchedDocuments([]);
            setFetchedPrefixes([""]);
          });
      }, []);


    return (
        <MainContext.Provider value={mainContextTools}>
            <div
                style={{
                    width: "100%",
                    minWidth: 1025,
                    height: "100vh",
                    minHeight: 700,
                    display: "flex",
                    flexDirection: "column",
                }}
            >
                <MainPageHeader />
                <Grid
                    container
                    justifyContent={"space-between"}
                    sx={{
                        borderBottom: "0.5px solid green",
                        overflow: "hidden",
                        minHeight: "30vh",
                    }}
                >
                    <Grid item xs={3} display={"flex"} flexDirection={"column"}>
                        <Container
                            sx={{
                                maxHeight: mode === "add" ? "74vh" : "53vh",
                                overflowY: "auto",
                            }}
                        >
                            <DocumentList documents={fetchedDocuments}/>
                        </Container>
                        <AddDocument mode={mode} setMode={setMode} prefixes={fetchedPrefixes} />
                    </Grid>
                    <Grid item xs={6} sx={{ height: "100%", overflow: "auto" }}>
                        <RequirementList />
                    </Grid>
                    <Grid item xs={0} />
                    <Grid item xs={2}>
                        <RequirementDetails />
                    </Grid>
                </Grid>
            </div>
        </MainContext.Provider>
    );
}
