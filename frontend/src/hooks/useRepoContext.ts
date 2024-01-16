import { useContext } from "react";
import { RepoContext } from "../App.tsx";

export type RepoContextType = {
    repositoryName: string | null;
    setRepositoryName: (repositoryName: string | null) => void;
};

export default function useRepoContext(): RepoContextType {
    const context = useContext(RepoContext);
    if (!context) {
        throw new Error(
            "useRepoContext must be used within a RepoContextProvider",
        );
    }
    return context;
}
