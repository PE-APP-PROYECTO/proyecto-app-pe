import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import BarraNavegacion from "../componentes/BarraNavegacion";
import { IlustracionInventario } from "../componentes/IconosSistema";
import TarjetaCategoria from "../componentes/TarjetaCategoria";
import TarjetaProducto from "../componentes/TarjetaProducto";
import { useAuth } from "../context/useAuth";
import { api } from "../services/api";
import { formatCurrency } from "../utils/format";

import "../home.css";

function Home() {
  const navigate = useNavigate();
  const { isAdmin } = useAuth();
  const [products, setProducts] = useState([]);
  const [brands, setBrands] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    Promise.all([
      api.getProducts({ limit: isAdmin ? 4 : 12, only_active: true }),
      api.getBrands(),
    ])
      .then(([productsData, brandsData]) => {
        if (!active) return;
        setProducts(productsData);
        setBrands(brandsData);
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
  }, [isAdmin]);

  const brandNames = new Map(brands.map((brand) => [brand.id, brand.name]));

  return (
    <div className="home-page">
      <BarraNavegacion />

      <main>
        <section className="hero-home">
          <div className="hero-text">
            <span className="hero-tag">TECNOLOGÍA PARA TI</span>
            <h1>Controla tu inventario tecnológico</h1>
            <p>
              Consulta productos, existencias, marcas y proveedores desde un
              solo lugar.
            </p>
            <button
              type="button"
              onClick={() =>
                isAdmin
                  ? navigate("/productos")
                  : document
                      .getElementById("productos-disponibles")
                      ?.scrollIntoView({ behavior: "smooth" })
              }
            >
              {isAdmin ? "Gestionar productos" : "Consultar productos"}
            </button>
          </div>
          <div className="hero-visual">
            <IlustracionInventario />
          </div>
        </section>

        {isAdmin && (
          <section className="categorias">
            <h2>Módulos de gestión</h2>
            <div className="contenedor-categorias">
              <button
                className="categoria-link"
                type="button"
                onClick={() => navigate("/productos")}
              >
                <TarjetaCategoria
                  tipoIcono="productos"
                  titulo="Productos y marcas"
                  descripcion="Inventario, precios, existencias y marcas"
                />
              </button>
              <button
                className="categoria-link"
                type="button"
                onClick={() => navigate("/proveedores")}
              >
                <TarjetaCategoria
                  tipoIcono="proveedores"
                  titulo="Proveedores"
                  descripcion="Datos de contacto y empresas proveedoras"
                />
              </button>
              <button
                className="categoria-link"
                type="button"
                onClick={() => navigate("/usuarios")}
              >
                <TarjetaCategoria
                  tipoIcono="usuarios"
                  titulo="Usuarios"
                  descripcion="Administración de cuentas del sistema"
                />
              </button>
            </div>
          </section>
        )}

        <section className="productos" id="productos-disponibles">
          <div className="titulo-seccion">
            <h2>{isAdmin ? "Productos recientes" : "Productos disponibles"}</h2>
            {isAdmin && (
              <button
                className="boton-enlace"
                type="button"
                onClick={() => navigate("/productos")}
              >
                Ver inventario
              </button>
            )}
          </div>

          {error && <div className="alerta alerta-error">{error}</div>}
          {loading && <p className="estado-carga">Cargando productos…</p>}
          {!loading && !error && products.length === 0 && (
            <p className="estado-carga">Todavía no hay productos registrados.</p>
          )}

          <div className="contenedor-productos">
            {products.map((product) => (
              <TarjetaProducto
                key={product.id}
                marca={brandNames.get(product.brand_id) || "Sin marca"}
                nombre={product.reference}
                descripcion={
                  product.description || `Color: ${product.color}`
                }
                precio={formatCurrency(product.price)}
                stock={product.stock}
                onView={
                  isAdmin
                    ? () =>
                        navigate(
                          `/productos?search=${encodeURIComponent(product.reference)}`,
                        )
                    : undefined
                }
              />
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default Home;
