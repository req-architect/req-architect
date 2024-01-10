import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import MainPage from "./pages/MainPage.tsx";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "react-confirm-alert/src/react-confirm-alert.css";
import AuthCallbackPage from "./pages/AuthCallbackPage.tsx";
import LoginPage from "./pages/LoginPage.tsx";

const router = createBrowserRouter([
    {
        path: "/main_page",
        element: <MainPage />,
    },
    {
        path: "/login_callback",
        element: <AuthCallbackPage />,
    },
    {
        path: "/",
        element: <LoginPage />,
    },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <RouterProvider router={router} />
        <ToastContainer />
    </React.StrictMode>,
);
