export async function PostDocument(prefix: string, parent?: string) {
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
}

export async function DeleteDocument(prefix: string) {
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
}

export async function fetchDocuments() {
    {
        try {
            const response = await fetch(
                "http://localhost:8000/MyServer/doc/",
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                },
            );
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
    }
}

export async function fetchRequirements(docPrefix: string) {
    {
        try {
            const response = await fetch(
                `http://localhost:8000/MyServer/req/?docId=${docPrefix}`,
                {
                    method: "GET",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                    },
                },
            );
            const data = await response.json();

            console.log("Fetched requirements:", data);
            return data;
        } catch (error: any) {
            if (error.message.includes("Internal Server Error")) {
                console.log("Couldn't fetch requirements:", error.message);
            } else if (error.message.includes("Unexpected token '<'")) {
                console.log("Empty document list");
            } else {
                console.error("Error fetching requirements:", error);
            }

            return [];
        }
    }
}
