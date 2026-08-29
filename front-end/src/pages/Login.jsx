import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../context/useAuth";

function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const { signIn, token } = useAuth();
  const [form, setForm] = useState({ username: "", password: "" });
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (token) navigate("/home", { replace: true });
  }, [navigate, token]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      await signIn(form.username.trim(), form.password, remember);
      navigate(location.state?.from || "/home", { replace: true });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <form className="login-card" onSubmit={handleSubmit}>
        <div className="logo">
          <h1>
            TEC<span>APP</span>
          </h1>
          <p>Gestión tecnológica inteligente</p>
        </div>

        <h2>Iniciar sesión</h2>

        {location.state?.registrationSuccess && (
          <div className="alerta alerta-exito">
            {location.state.registrationSuccess}
          </div>
        )}
        {error && <div className="alerta alerta-error">{error}</div>}

        <div className="input-group">
          <label htmlFor="username">Usuario</label>
          <input
            id="username"
            name="username"
            type="text"
            value={form.username}
            onChange={(event) =>
              setForm((current) => ({
                ...current,
                username: event.target.value,
              }))
            }
            placeholder="Ingresa tu usuario"
            autoComplete="username"
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="password">Contraseña</label>
          <input
            id="password"
            name="password"
            type="password"
            value={form.password}
            onChange={(event) =>
              setForm((current) => ({
                ...current,
                password: event.target.value,
              }))
            }
            placeholder="••••••••"
            autoComplete="current-password"
            required
          />
        </div>

        <label className="remember-option">
          <input
            type="checkbox"
            checked={remember}
            onChange={(event) => setRemember(event.target.checked)}
          />
          Mantener la sesión en este equipo
        </label>

        <button className="login-button" type="submit" disabled={loading}>
          {loading ? "Ingresando…" : "Ingresar"}
        </button>

        <p className="auth-alternative">
          ¿No tienes una cuenta? <Link to="/registro">Crear cuenta</Link>
        </p>
      </form>
    </div>
  );
}

export default Login;
