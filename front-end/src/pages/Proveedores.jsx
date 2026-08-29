import { useEffect, useMemo, useState } from "react";

import BarraNavegacion from "../componentes/BarraNavegacion";
import { api } from "../services/api";

import "../admin.css";

const EMPTY_PROVIDER = {
  company_name: "",
  nit: "",
  phone: "",
  email: "",
  address: "",
};

function Proveedores() {
  const [providers, setProviders] = useState([]);
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
      .getProviders()
      .then((data) => {
        if (active) setProviders(data);
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

  const filteredProviders = useMemo(() => {
    const term = search.trim().toLocaleLowerCase("es");
    if (!term) return providers;
    return providers.filter((provider) =>
      [
        provider.company_name,
        provider.nit,
        provider.email,
        provider.phone,
      ].some((value) => String(value || "").toLocaleLowerCase("es").includes(term)),
    );
  }, [providers, search]);

  const openCreate = () => {
    setEditingId(null);
    setForm(EMPTY_PROVIDER);
    setError("");
    setMessage("");
  };

  const openEdit = (provider) => {
    setEditingId(provider.id);
    setForm({
      company_name: provider.company_name,
      nit: provider.nit,
      phone: provider.phone || "",
      email: provider.email,
      address: provider.address || "",
    });
    setError("");
    setMessage("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");

    const payload = Object.fromEntries(
      Object.entries(form).map(([key, value]) => [key, value.trim()]),
    );

    try {
      if (editingId) {
        await api.updateProvider(editingId, payload);
        setMessage("Proveedor actualizado.");
      } else {
        await api.createProvider(payload);
        setMessage("Proveedor creado.");
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

  const handleDelete = async (provider) => {
    if (
      !window.confirm(
        `¿Desactivar el proveedor ${provider.company_name}? Esta acción fallará si tiene productos activos.`,
      )
    ) {
      return;
    }

    try {
      await api.deleteProvider(provider.id);
      setMessage("Proveedor desactivado.");
      setError("");
      setLoading(true);
      setReload((current) => current + 1);
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
            <span className="eyebrow">DIRECTORIO</span>
            <h1>Proveedores</h1>
            <p>Administra las empresas que suministran los productos.</p>
          </div>
          <button className="boton-primario" type="button" onClick={openCreate}>
            Nuevo proveedor
          </button>
        </div>

        {error && <div className="alerta alerta-error">{error}</div>}
        {message && <div className="alerta alerta-exito">{message}</div>}

        {form && (
          <section className="panel formulario-panel">
            <div className="panel-titulo">
              <h2>{editingId ? "Editar proveedor" : "Crear proveedor"}</h2>
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
                Razón social
                <input
                  value={form.company_name}
                  onChange={(event) =>
                    setForm((current) => ({
                      ...current,
                      company_name: event.target.value,
                    }))
                  }
                  minLength="5"
                  maxLength="100"
                  required
                />
              </label>
              <label>
                NIT
                <input
                  value={form.nit}
                  onChange={(event) =>
                    setForm((current) => ({
                      ...current,
                      nit: event.target.value,
                    }))
                  }
                  pattern="[0-9\-]{8,12}"
                  title="Use entre 8 y 12 números o guiones"
                  required
                />
              </label>
              <label>
                Teléfono
                <input
                  value={form.phone}
                  onChange={(event) =>
                    setForm((current) => ({
                      ...current,
                      phone: event.target.value,
                    }))
                  }
                  pattern="\+?[0-9]{8,13}"
                  title="Use entre 8 y 13 números; puede iniciar con +"
                  required
                />
              </label>
              <label>
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
              <label className="campo-completo">
                Dirección
                <input
                  value={form.address}
                  onChange={(event) =>
                    setForm((current) => ({
                      ...current,
                      address: event.target.value,
                    }))
                  }
                  maxLength="100"
                  required
                />
              </label>
              <div className="acciones-form campo-completo">
                <button className="boton-primario" type="submit" disabled={saving}>
                  {saving ? "Guardando…" : "Guardar proveedor"}
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
              <h2>Directorio de proveedores</h2>
              <p>{filteredProviders.length} registro(s)</p>
            </div>
            <input
              className="busqueda-tabla"
              type="search"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Buscar empresa, NIT o correo"
            />
          </div>

          {loading ? (
            <p className="estado-carga">Cargando proveedores…</p>
          ) : (
            <div className="tabla-contenedor">
              <table>
                <thead>
                  <tr>
                    <th>Empresa</th>
                    <th>NIT</th>
                    <th>Contacto</th>
                    <th>Dirección</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredProviders.map((provider) => (
                    <tr key={provider.id}>
                      <td>
                        <strong>{provider.company_name}</strong>
                        <small>ID: {provider.id}</small>
                      </td>
                      <td>{provider.nit}</td>
                      <td>
                        {provider.email}
                        <small>{provider.phone || "Sin teléfono"}</small>
                      </td>
                      <td>{provider.address || "Sin dirección"}</td>
                      <td>
                        <div className="acciones-tabla">
                          <button type="button" onClick={() => openEdit(provider)}>
                            Editar
                          </button>
                          <button
                            className="accion-peligro"
                            type="button"
                            onClick={() => handleDelete(provider)}
                          >
                            Desactivar
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {!filteredProviders.length && (
                    <tr>
                      <td className="tabla-vacia" colSpan="5">
                        No hay proveedores para mostrar.
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

export default Proveedores;
