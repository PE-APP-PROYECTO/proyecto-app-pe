import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "../context/useAuth";
import "../navigation.css";

function BarraNavegacion() {
  const navigate = useNavigate();
  const { isAdmin, signOut, username } = useAuth();
  const [search, setSearch] = useState("");

  const handleSearch = (event) => {
    event.preventDefault();
    const query = search.trim();
    navigate(query ? `/productos?search=${encodeURIComponent(query)}` : "/productos");
  };

  const handleLogout = () => {
    signOut();
    navigate("/", { replace: true });
  };

  return (
    <>
      <header className="barra-superior">
        <NavLink className="logo-tecapp" to="/home">
          TEC<span>APP</span>
        </NavLink>

        {isAdmin && (
          <form className="buscador" onSubmit={handleSearch}>
            <input
              type="search"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Buscar por referencia, color o descripción…"
              aria-label="Buscar productos"
            />
            <button type="submit">Buscar</button>
          </form>
        )}

        <div className="usuario">
          <span title={username}>{isAdmin ? "Administrador" : username}</span>
          <button className="boton-salir" type="button" onClick={handleLogout}>
            Salir
          </button>
        </div>
      </header>

      <nav className="menu" aria-label="Navegación principal">
        <NavLink to="/home">Inicio</NavLink>
        {isAdmin && (
          <>
            <NavLink to="/productos">Productos y marcas</NavLink>
            <NavLink to="/proveedores">Proveedores</NavLink>
            <NavLink to="/usuarios">Usuarios</NavLink>
          </>
        )}
      </nav>
    </>
  );
}

export default BarraNavegacion;
