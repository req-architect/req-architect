
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

  
