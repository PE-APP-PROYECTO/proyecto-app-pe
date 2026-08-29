import { useEffect, useMemo, useState } from "react";

import BarraNavegacion from "../componentes/BarraNavegacion";
import { api } from "../services/api";

import "../admin.css";

const EMPTY_USER = {
  fullName: "",
  email: "",
  document: "",
  password: "",
  confirm_password: "",
};

function Usuarios() {
  const [users, setUsers] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [form, setForm] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [reload, setReload] = useState(0);

  useEffect(() => {
    let active = true;

    api
      .getUsers()
      .then((data) => {
        if (active) setUsers(data);
      })
      .catch((requestError) => {
        if (active) setError(requestError.message);
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [reload]);

  const filteredUsers = useMemo(() => {
    const term = search.trim().toLocaleLowerCase("es");
    if (!term) return users;
    return users.filter((user) =>
      [user.full_name, user.email, user.document].some((value) =>
        String(value || "").toLocaleLowerCase("es").includes(term),
      ),
    );
  }, [search, users]);

  const openCreate = () => {
    setEditingId(null);
    setForm(EMPTY_USER);
    setError("");
    setMessage("");
  };

  const openEdit = (user) => {
    setEditingId(user.id);
    setForm({
      ...EMPTY_USER,
      fullName: user.full_name,
      email: user.email,
      document: user.document || "",
    });
    setError("");
    setMessage("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");

    try {
      if (editingId) {
        await api.updateUser(editingId, {
          fullName: form.fullName.trim(),
          email: form.email.trim(),
          document: form.document.trim(),
        });
        setMessage("Usuario actualizado.");
      } else {
        await api.createUser({
          fullName: form.fullName.trim(),
          email: form.email.trim(),
          document: form.document.trim(),
          password: form.password,
          confirm_password: form.confirm_password,
        });
        setMessage("Usuario creado.");
      }
      setForm(null);
      setEditingId(null);
      setError("");
      setLoading(true);
      setReload((current) => current + 1);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (user) => {
    if (!window.confirm(`¿Desactivar al usuario ${user.full_name}?`)) return;

    try {
      await api.deleteUser(user.id);
      setUsers((current) => current.filter((item) => item.id !== user.id));
      setMessage("Usuario desactivado.");
      setError("");
    } catch (requestError) {
      setError(requestError.message);
    }
  };

  return (
    <div className="admin-page">
      <BarraNavegacion />
      <main className="admin-main">
        <div className="encabezado-pagina">
          <div>
            <span className="eyebrow">ADMINISTRACIÓN</span>
            <h1>Usuarios</h1>
            <p>Crea y actualiza las cuentas almacenadas por el sistema.</p>
          </div>
          <button className="boton-primario" type="button" onClick={openCreate}>
            Nuevo usuario
          </button>
        </div>

        {error && <div className="alerta alerta-error">{error}</div>}
        {message && <div className="alerta alerta-exito">{message}</div>}

        {form && (
          <section className="panel formulario-panel">
            <div className="panel-titulo">
              <h2>{editingId ? "Editar usuario" : "Crear usuario"}</h2>
              <button
                className="boton-texto"
                type="button"
                onClick={() => setForm(null)}
              >
                Cerrar
              </button>
            </div>

            <form className="form-grid" onSubmit={handleSubmit}>
              <label>
                Nombre completo
                <input
                  value={form.fullName}
                  onChange={(event) =>
                    setForm((current) => ({
                      ...current,
                      fullName: event.target.value,
                    }))
                  }
                  minLength="3"
                  maxLength="50"
                  required
                />
              </label>
              <label>
                Documento
                <input
                  value={form.document}
                  onChange={(event) =>
                    setForm((current) => ({
                      ...current,
                      document: event.target.value,
                    }))
                  }
                  minLength="6"
                  maxLength="11"
                  required
                />
              </label>
              <label className="campo-completo">
                Correo electrónico
                <input
                  type="email"
                  value={form.email}
                  onChange={(event) =>
                    setForm((current) => ({
                      ...current,
                      email: event.target.value,
                    }))
                  }
                  required
                />
              </label>

              {!editingId && (
                <>
                  <label>
                    Contraseña
                    <input
                      type="password"
                      value={form.password}
                      onChange={(event) =>
                        setForm((current) => ({
                          ...current,
                          password: event.target.value,
                        }))
                      }
                      minLength="8"
                      maxLength="50"
                      autoComplete="new-password"
                      required
                    />
                  </label>
                  <label>
                    Confirmar contraseña
                    <input
                      type="password"
                      value={form.confirm_password}
                      onChange={(event) =>
                        setForm((current) => ({
                          ...current,
                          confirm_password: event.target.value,
                        }))
                      }
                      minLength="8"
                      maxLength="50"
                      autoComplete="new-password"
                      required
                    />
                  </label>
                </>
              )}

              <div className="acciones-form campo-completo">
                <button className="boton-primario" type="submit" disabled={saving}>
                  {saving ? "Guardando…" : "Guardar usuario"}
                </button>
                <button
                  className="boton-secundario"
                  type="button"
                  onClick={() => setForm(null)}
                >
                  Cancelar
                </button>
              </div>
            </form>
          </section>
        )}

        <section className="panel">
          <div className="panel-titulo panel-titulo-responsive">
            <div>
              <h2>Usuarios registrados</h2>
              <p>{filteredUsers.length} registro(s)</p>
            </div>
            <input
              className="busqueda-tabla"
              type="search"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Buscar nombre, correo o documento"
            />
          </div>

          {loading ? (
            <p className="estado-carga">Cargando usuarios…</p>
          ) : (
            <div className="tabla-contenedor">
              <table>
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>Documento</th>
                    <th>Correo electrónico</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((user) => (
                    <tr key={user.id}>
                      <td>
                        <strong>{user.full_name}</strong>
                        <small>ID: {user.id}</small>
                      </td>
                      <td>{user.document || "Sin documento"}</td>
                      <td>{user.email}</td>
                      <td>
                        <div className="acciones-tabla">
                          <button type="button" onClick={() => openEdit(user)}>
                            Editar
                          </button>
                          <button
                            className="accion-peligro"
                            type="button"
                            onClick={() => handleDelete(user)}
                          >
                            Desactivar
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {!filteredUsers.length && (
                    <tr>
                      <td className="tabla-vacia" colSpan="4">
                        No hay usuarios para mostrar.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default Usuarios;
