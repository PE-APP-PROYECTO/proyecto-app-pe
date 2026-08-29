import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { AuthProvider } from "./context/AuthProvider";
import Chatbot from "./componentes/Chatbot";
import RutaProtegida from "./componentes/RutaProtegida";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Productos from "./pages/Productos";
import Proveedores from "./pages/Proveedores";
import Registro from "./pages/Registro";
import Usuarios from "./pages/Usuarios";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/registro" element={<Registro />} />
          <Route
            path="/home"
            element={
              <RutaProtegida>
                <Home />
              </RutaProtegida>
            }
          />
          <Route
            path="/productos"
            element={
              <RutaProtegida allowedRoles={["admin"]}>
                <Productos />
              </RutaProtegida>
            }
          />
          <Route
            path="/proveedores"
            element={
              <RutaProtegida allowedRoles={["admin"]}>
                <Proveedores />
              </RutaProtegida>
            }
          />
          <Route
            path="/usuarios"
            element={
              <RutaProtegida allowedRoles={["admin"]}>
                <Usuarios />
              </RutaProtegida>
            }
          />
          <Route path="*" element={<Navigate to="/home" replace />} />
        </Routes>
        <Chatbot />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
