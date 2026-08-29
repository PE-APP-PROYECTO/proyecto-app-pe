import { Navigate, useLocation } from "react-router-dom";

import { useAuth } from "../context/useAuth";

function RutaProtegida({ children, allowedRoles }) {
  const { role, token } = useAuth();
  const location = useLocation();

  if (!token) {
    return <Navigate to="/" replace state={{ from: location.pathname }} />;
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
    return <Navigate to="/home" replace />;
  }

  return children;
}

export default RutaProtegida;
