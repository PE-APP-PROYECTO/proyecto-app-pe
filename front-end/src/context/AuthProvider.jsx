import { useEffect, useMemo, useState } from "react";

import { api, clearStoredToken, getStoredToken } from "../services/api";
import { AuthContext } from "./authContext";

function readTokenPayload(token) {
  if (!token) return null;

  try {
    const payload = token.split(".")[1];
    const normalized = payload.replace(/-/g, "+").replace(/_/g, "/");
    const padded = normalized.padEnd(
      normalized.length + ((4 - (normalized.length % 4)) % 4),
      "=",
    );
    const decoded = decodeURIComponent(
      window
        .atob(padded)
        .split("")
        .map((character) =>
          `%${character.charCodeAt(0).toString(16).padStart(2, "0")}`,
        )
        .join(""),
    );
    return JSON.parse(decoded);
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => getStoredToken());
  const session = useMemo(() => readTokenPayload(token), [token]);

  useEffect(() => {
    const handleUnauthorized = () => setToken(null);
    window.addEventListener("tecapp:unauthorized", handleUnauthorized);
    return () =>
      window.removeEventListener("tecapp:unauthorized", handleUnauthorized);
  }, []);

  const value = useMemo(
    () => ({
      token,
      role: session?.role || null,
      username: session?.sub || "Usuario",
      isAdmin: session?.role === "admin",
      async signIn(username, password, remember) {
        const result = await api.login(username, password, remember);
        setToken(result.access_token);
      },
      signOut() {
        clearStoredToken();
        setToken(null);
      },
    }),
    [session, token],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
