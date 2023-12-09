import { ReqDocument, ReqDocumentWithChildren } from "../types";


export function PostDocument (prefix: String, parent?: String) {
    console.log("Sending data:", prefix, parent);
    fetch("http://localhost:8000/MyServer/doc/", {
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

  
