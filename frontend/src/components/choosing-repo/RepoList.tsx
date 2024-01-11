import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import { getRepos } from "../../lib/api/gitService";
import { useEffect, useState } from "react";

export default function RepoList({
    onRepoSelected,
}: {
    onRepoSelected: (repo: string) => void;
}) {
    const [repositories, setRepositories] = useState<string[]>([]);
    const [selectedRepo, setSelectedRepo] = useState<string | null>(null);

    useEffect(() => {
        async function fetchUserRepos() {
            try {
                const repos = await getRepos();
                setRepositories(repos);
            } catch (error) {
                console.error("Error fetching repositories:", error);
            }
        }
        fetchUserRepos();
        onRepoSelected(repositories[0]);
    }, []);

    return (
        <Autocomplete
            value={selectedRepo}
            disablePortal
            onChange={(_, value) => {
                if (value) {
                    setSelectedRepo(value);
                    onRepoSelected(value);
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
