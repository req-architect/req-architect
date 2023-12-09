import { useState } from "react";
import { RenderTree } from "../components/main/DocumentList";

export async function PostDocument (prefix: String, parent?: String) {
    console.log("Sending data:", prefix, parent);
    await fetch("http://localhost:8000/MyServer/doc/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({

            docId: prefix,
            ...(parent && { parentId: parent }),
        }),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then((data) => {
        console.log(data);
    })
    .catch((error) => {
        console.error("Error adding document:", error);
    });
};

export async function DeleteDocument (prefix: String) {
    console.log("Deleting data:", prefix);
    await fetch("http://localhost:8000/MyServer/doc/", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({

            docId: prefix,
        }),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then((data) => {
        console.log(data);
    })
    .catch((error) => {
        console.error("Error deleting document:", error);
    });
};

const extractPrefixes = (document: { prefix: string; children?: any[] }) => {
    let prefixes: string[] = [document.prefix];

    if (document.children && document.children.length > 0) {
        document.children.forEach((child) => {
            prefixes = [...prefixes, ...extractPrefixes(child)];
        });
    }
    return prefixes;
};

  
export async function  fetchDocuments() {
{
        try {
            const response = await fetch("http://localhost:8000/MyServer/doc/", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });
            const data = await response.json();
    
            console.log("Fetched documents:", data);
            return data;
        } catch (error: any) {
            if (error.message.includes("Internal Server Error")) {
                console.log("Couldn't fetch documents:", error.message);
            } else if (error.message.includes("Unexpected token '<'")) {
                console.log("Empty document list");
            } else {
                console.error("Error fetching documents:", error);
            }
    
            return [];
        }
}}