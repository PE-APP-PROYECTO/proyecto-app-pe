import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { api } from "../services/api";

const EMPTY_FORM = {
  fullName: "",
  email: "",
  document: "",
  password: "",
  confirm_password: "",
};

function Registro() {
  const navigate = useNavigate();
  const [form, setForm] = useState(EMPTY_FORM);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const updateField = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (form.password !== form.confirm_password) {
      setError("Las contraseñas no coinciden.");
      return;
    }

    setLoading(true);
    try {
      await api.registerUser({
        fullName: form.fullName.trim(),
        email: form.email.trim(),
        document: form.document.trim(),
        password: form.password,
        confirm_password: form.confirm_password,
      });

      navigate("/", {
        replace: true,
        state: {
          registrationSuccess:
            "Cuenta creada correctamente. Ya puedes iniciar sesión.",
        },
      });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <form className="login-card registro-card" onSubmit={handleSubmit}>
        <div className="logo logo-compacto">
          <h1>
            TEC<span>APP</span>
          </h1>
          <p>Gestión tecnológica inteligente</p>
        </div>

        <div className="auth-heading">
          <h2>Crear cuenta</h2>
          <p>Completa tus datos para registrarte.</p>
        </div>

        {error && <div className="alerta alerta-error">{error}</div>}

        <div className="registro-grid">
          <div className="input-group">
            <label htmlFor="fullName">Nombre completo</label>
            <input
              id="fullName"
              name="fullName"
              type="text"
              value={form.fullName}
              onChange={updateField}
              minLength="3"
              maxLength="50"
              autoComplete="name"
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="document">Documento</label>
            <input
              id="document"
              name="document"
              type="text"
              value={form.document}
              onChange={updateField}
              minLength="6"
              maxLength="11"
              inputMode="numeric"
              autoComplete="off"
              required
            />
          </div>

          <div className="input-group campo-auth-completo">
            <label htmlFor="email">Correo electrónico</label>
            <input
              id="email"
              name="email"
              type="email"
              value={form.email}
              onChange={updateField}
              autoComplete="email"
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="new-password">Contraseña</label>
            <input
              id="new-password"
              name="password"
              type="password"
              value={form.password}
              onChange={updateField}
              minLength="8"
              maxLength="50"
              autoComplete="new-password"
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="confirm-password">Confirmar contraseña</label>
            <input
              id="confirm-password"
              name="confirm_password"
              type="password"
              value={form.confirm_password}
              onChange={updateField}
              minLength="8"
              maxLength="50"
              autoComplete="new-password"
              required
            />
          </div>
        </div>

        <button className="login-button" type="submit" disabled={loading}>
          {loading ? "Creando cuenta…" : "Crear cuenta"}
        </button>

        <p className="auth-alternative">
          ¿Ya tienes una cuenta? <Link to="/">Inicia sesión</Link>
        </p>
      </form>
    </div>
  );
}

export default Registro;
