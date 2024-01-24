import { createBrowserRouter, RouterProvider } from "react-router-dom";
import MainPage from "./pages/MainPage.tsx";
import AuthCallbackPage from "./pages/AuthCallbackPage.tsx";
import LoginPage from "./pages/LoginPage.tsx";
import ChoosingRepoPage from "./pages/ChoosingRepoPage.tsx";
import { ToastContainer } from "react-toastify";
import useAuthContext, { AuthContextTools } from "./hooks/useAuthContext.ts";
import { createContext, useState } from "react";
import { RepoContextType } from "./hooks/useRepoContext.ts";

const router = createBrowserRouter([
    {
        path: "/",
        element: <MainPage />,
    },
    {
        path: "/login_callback",
        element: <AuthCallbackPage />,
    },
    {
        path: "/login",
        element: <LoginPage />,
    },
    {
        path: "/repo",
        element: <ChoosingRepoPage />,
    },
]);

export const AuthContext = createContext<AuthContextTools | null>(null);

export const RepoContext = createContext<RepoContextType | null>(null);

export default function App() {
    const authTools = useAuthContext();
    const [repositoryName, setRepositoryName] = useState<string | null>(null);
    return (
        <AuthContext.Provider value={authTools}>
            <RepoContext.Provider value={{ repositoryName, setRepositoryName }}>
                <RouterProvider router={router} />
                <ToastContainer position="bottom-right" />
            </RepoContext.Provider>
        </AuthContext.Provider>
    );
}
