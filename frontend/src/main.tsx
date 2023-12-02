import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import MainPage from "./pages/MainPage.tsx";
import ChoosingRepoPage from "./pages/ChoosingRepoPage.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <ChoosingRepoPage />,
  },
  {
    path: "/main",
    element: <MainPage />,
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

process.on("SIGINT", function () {
  console.log("\nGracefully shutting down from SIGINT (Ctrl-C)");
  // some other closing procedures go here
  process.exit(0);
});
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode></React.StrictMode>
);
