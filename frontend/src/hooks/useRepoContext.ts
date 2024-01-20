import { useContext } from "react";
import { RepoContext } from "../App.tsx";

/* 
    This hook is used to manage the repository context of the application.
    It is used to manage the selected repository.
    It also provides functions to update the context.
*/

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
