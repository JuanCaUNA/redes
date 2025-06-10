// src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./css/index.css";

import Login from "./pages/Login";
import { Layout } from "./components/Layout";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        {/* Login por defecto */}
        <Route path="/" element={<Login />} />

        {/* App protegida, renderizada solo si hay sesión */}
        <Route path="/app" element={<Layout />} />

        {/* Redirección general */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
