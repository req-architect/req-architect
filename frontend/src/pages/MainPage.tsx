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
import { fetchDocuments } from "../hooks/MainFunctions.ts";

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
    
    const updatePrefixes = () => {
        if (fetchedPrefixes.length > 1) {
            const uniqueOptions = Array.from(new Set(fetchedPrefixes)).sort((a, b) => a.localeCompare(b));
            setFetchedPrefixes(uniqueOptions);
          }
    };
    
    async function getDocuments  () {
        // Fetch documents from Django backend
        const data = await fetchDocuments();
        console.log("Fetched documents:", data);
        setFetchedPrefixes([]);
        setFetchedDocuments(data);
        data.forEach((document: { prefix: string; children?: any[] | undefined; }) => {
        const documentPrefixes = extractPrefixes(document);
        setFetchedPrefixes((prevPrefixes) => [...prevPrefixes, ...documentPrefixes]);
    });
    };
      
      useEffect(() => {
        getDocuments();
      }, []);
      
      const handleDeleteDocument = async () => {
        await getDocuments();
      };
      
      const handleAddDocument = async () => {
        await getDocuments();
      }
      
      useEffect(() => {
        updatePrefixes();
    }, [fetchedDocuments]);


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
                        height: "95vh",
                    }}
                >
                    <Grid item xs={2} display={"flex"} flexDirection={"column"} borderRight={"1px solid green"}>
                        <DocumentList documents={fetchedDocuments} onDeleteDocument={handleDeleteDocument}/>
                        <AddDocument mode={mode} setMode={setMode} prefixes={fetchedPrefixes} onAddDocument={handleAddDocument} />
                    </Grid>
                    <Grid item xs={8} sx={{ height: "100%", overflow: "auto", paddingRight: 8 , paddingLeft: 8}}>
                        <RequirementList />
                    </Grid>
                    {/* <Grid item xs={1} /> */}
                    <Grid item xs={2}>
                        <RequirementDetails />
                    </Grid>
                </Grid>
            </div>
        </MainContext.Provider>
    );
}
