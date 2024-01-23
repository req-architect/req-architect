import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import { getRepos } from "../../lib/api/gitService";
import { useEffect, useState } from "react";
import { useAuth } from "../../hooks/useAuthContext.ts";
import { APIError } from "../../lib/api/fetchAPI.ts";
import { toast } from "react-toastify";

/*
    This component is used to display a list of repositories to the user.
    It will fetch the repositories from the API and display them in a dropdown.
*/

export default function RepoList({
    chosenRepository,
    setChosenRepository,
}: {
    chosenRepository: string | null;
    setChosenRepository: (repo: string | null) => void;
}) {
    const [repositories, setRepositories] = useState<string[]>([]);
    const authTools = useAuth();

    useEffect(() => {
        if (!authTools.tokenStr) {
            return;
        }
        getRepos(authTools.tokenStr)
            .then(setRepositories)
            .catch((e) => {
                if (e instanceof APIError) {
                    toast.error(e.message);
                    return;
                }
                toast.error(
                    `An error occurred while fetching your identity: ${e.name}`,
                );
                console.error(e);
            });
    }, [authTools]);

    return (
        <Autocomplete
            value={chosenRepository}
            disablePortal
            onChange={(_, value) => {
                if (value) {
                    setChosenRepository(value);
                }
            }}
            renderInput={(params) => (
                <TextField {...params} label="Repository" />
            )}
            options={repositories.sort((a, b) => -b.localeCompare(a))}
            sx={{ width: "70%", mt: "auto", mb: 10, alignSelf: "center" }}
        />
    );
}
