import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";

import BarraNavegacion from "../componentes/BarraNavegacion";
import { api } from "../services/api";
import { formatCurrency } from "../utils/format";

import "../admin.css";

const EMPTY_PRODUCT = {
  reference: "",
  price: "",
  color: "",
  brand_id: "",
  stock: "",
  description: "",
  provider_id: "",
};

const EMPTY_BRAND = {
  name: "",
  description: "",
};

function Productos() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialSearch = searchParams.get("search") || "";
  const [search, setSearch] = useState(initialSearch);
  const [appliedSearch, setAppliedSearch] = useState(initialSearch);
  const [products, setProducts] = useState([]);
  const [brands, setBrands] = useState([]);
  const [providers, setProviders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [reload, setReload] = useState(0);
  const [productForm, setProductForm] = useState(null);
  const [editingProductId, setEditingProductId] = useState(null);
  const [brandForm, setBrandForm] = useState(EMPTY_BRAND);
  const [editingBrandId, setEditingBrandId] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    let active = true;

    Promise.all([
      api.getProducts({
        limit: 500,
        only_active: true,
        search: appliedSearch,
      }),
      api.getBrands(),
      api.getProviders(),
    ])
      .then(([productsData, brandsData, providersData]) => {
        if (!active) return;
        setProducts(productsData);
        setBrands(brandsData);
        setProviders(providersData);
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
  }, [appliedSearch, reload]);

  const brandNames = useMemo(
    () => new Map(brands.map((brand) => [brand.id, brand.name])),
    [brands],
  );
  const providerNames = useMemo(
    () =>
      new Map(
        providers.map((provider) => [provider.id, provider.company_name]),
      ),
    [providers],
  );

  const refresh = (successMessage) => {
    setMessage(successMessage);
    setError("");
    setLoading(true);
    setReload((current) => current + 1);
  };

  const handleSearch = (event) => {
    event.preventDefault();
    const value = search.trim();
    setLoading(true);
    setError("");
    setAppliedSearch(value);
    setSearchParams(value ? { search: value } : {});
  };

  const openCreateProduct = () => {
    setMessage("");
    setError("");
    if (!brands.length || !providers.length) {
      setError(
        "Para crear un producto debe existir al menos una marca y un proveedor.",
      );
      return;
    }
    setEditingProductId(null);
    setProductForm({
      ...EMPTY_PRODUCT,
      brand_id: String(brands[0].id),
      provider_id: String(providers[0].id),
    });
  };

  const openEditProduct = (product) => {
    setEditingProductId(product.id);
    setProductForm({
      reference: product.reference,
      price: String(product.price),
      color: product.color,
      brand_id: String(product.brand_id),
      stock: String(product.stock),
      description: product.description || "",
      provider_id: String(product.provider_id),
    });
    setMessage("");
    setError("");
  };

  const handleProductSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");

    const payload = {
      ...productForm,
      price: Number(productForm.price),
      stock: Number(productForm.stock),
      brand_id: Number(productForm.brand_id),
      provider_id: Number(productForm.provider_id),
      description: productForm.description.trim(),
    };

    try {
      if (editingProductId) {
        await api.updateProduct(editingProductId, payload);
        refresh("Producto actualizado.");
      } else {
        await api.createProduct(payload);
        refresh("Producto creado.");
      }
      setProductForm(null);
      setEditingProductId(null);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteProduct = async (product) => {
    if (!window.confirm(`¿Desactivar el producto ${product.reference}?`)) {
      return;
    }

    try {
      await api.deleteProduct(product.id);
      refresh("Producto desactivado.");
    } catch (requestError) {
      setError(requestError.message);
    }
  };

  const handleBrandSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");

    const payload = {
      name: brandForm.name.trim(),
      description: brandForm.description.trim(),
    };

    try {
      if (editingBrandId) {
        await api.updateBrand(editingBrandId, payload);
        refresh("Marca actualizada.");
      } else {
        await api.createBrand(payload);
        refresh("Marca creada.");
      }
      setBrandForm(EMPTY_BRAND);
      setEditingBrandId(null);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setSaving(false);
    }
  };

  const editBrand = (brand) => {
    setEditingBrandId(brand.id);
    setBrandForm({
      name: brand.name,
      description: brand.description || "",
    });
    setMessage("");
    setError("");
  };

  const handleDeleteBrand = async (brand) => {
    if (!window.confirm(`¿Desactivar la marca ${brand.name}?`)) return;

    try {
      await api.deleteBrand(brand.id);
      refresh("Marca desactivada.");
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
            <span className="eyebrow">INVENTARIO</span>
            <h1>Productos y marcas</h1>
            <p>Los datos de esta pantalla se consultan directamente en la API.</p>
          </div>
          <button className="boton-primario" type="button" onClick={openCreateProduct}>
            Nuevo producto
          </button>
        </div>

        {error && <div className="alerta alerta-error">{error}</div>}
        {message && <div className="alerta alerta-exito">{message}</div>}

        {productForm && (
          <section className="panel formulario-panel">
            <div className="panel-titulo">
              <h2>
                {editingProductId ? "Editar producto" : "Crear producto"}
              </h2>
              <button
                className="boton-texto"
                type="button"
                onClick={() => setProductForm(null)}
              >
                Cerrar
              </button>
            </div>
            <form className="form-grid" onSubmit={handleProductSubmit}>
              <label>
                Referencia
                <input
                  value={productForm.reference}
                  onChange={(event) =>
                    setProductForm((current) => ({
                      ...current,
                      reference: event.target.value,
                    }))
                  }
                  minLength="3"
                  maxLength="30"
                  required
                />
              </label>
              <label>
                Precio
                <input
                  type="number"
                  value={productForm.price}
                  onChange={(event) =>
                    setProductForm((current) => ({
                      ...current,
                      price: event.target.value,
                    }))
                  }
                  min="0"
                  step="1"
                  required
                />
              </label>
              <label>
                Color
                <input
                  value={productForm.color}
                  onChange={(event) =>
                    setProductForm((current) => ({
                      ...current,
                      color: event.target.value,
                    }))
                  }
                  minLength="2"
                  maxLength="20"
                  required
                />
              </label>
              <label>
                Existencias
                <input
                  type="number"
                  value={productForm.stock}
                  onChange={(event) =>
                    setProductForm((current) => ({
                      ...current,
                      stock: event.target.value,
                    }))
                  }
                  min="0"
                  step="1"
                  required
                />
              </label>
              <label>
                Marca
                <select
                  value={productForm.brand_id}
                  onChange={(event) =>
                    setProductForm((current) => ({
                      ...current,
                      brand_id: event.target.value,
                    }))
                  }
                  required
                >
                  {brands.map((brand) => (
                    <option key={brand.id} value={brand.id}>
                      {brand.name}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Proveedor
                <select
                  value={productForm.provider_id}
                  onChange={(event) =>
                    setProductForm((current) => ({
                      ...current,
                      provider_id: event.target.value,
                    }))
                  }
                  required
                >
                  {providers.map((provider) => (
                    <option key={provider.id} value={provider.id}>
                      {provider.company_name}
                    </option>
                  ))}
                </select>
              </label>
              <label className="campo-completo">
                Descripción
                <textarea
                  value={productForm.description}
                  onChange={(event) =>
                    setProductForm((current) => ({
                      ...current,
                      description: event.target.value,
                    }))
                  }
                  maxLength="100"
                  rows="3"
                  required
                />
              </label>
              <div className="acciones-form campo-completo">
                <button className="boton-primario" type="submit" disabled={saving}>
                  {saving ? "Guardando…" : "Guardar producto"}
                </button>
                <button
                  className="boton-secundario"
                  type="button"
                  onClick={() => setProductForm(null)}
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
              <h2>Inventario</h2>
              <p>{products.length} registro(s) encontrado(s)</p>
            </div>
            <form className="filtro" onSubmit={handleSearch}>
              <input
                type="search"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Referencia, descripción o color"
              />
              <button className="boton-secundario" type="submit">
                Buscar
              </button>
            </form>
          </div>

          {loading ? (
            <p className="estado-carga">Cargando inventario…</p>
          ) : (
            <div className="tabla-contenedor">
              <table>
                <thead>
                  <tr>
                    <th>Referencia</th>
                    <th>Marca</th>
                    <th>Color</th>
                    <th>Precio</th>
                    <th>Stock</th>
                    <th>Proveedor</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {products.map((product) => (
                    <tr key={product.id}>
                      <td>
                        <strong>{product.reference}</strong>
                        <small>{product.description || "Sin descripción"}</small>
                      </td>
                      <td>{brandNames.get(product.brand_id) || product.brand_id}</td>
                      <td>{product.color}</td>
                      <td>{formatCurrency(product.price)}</td>
                      <td>
                        <span
                          className={
                            product.stock > 0
                              ? "badge badge-activo"
                              : "badge badge-alerta"
                          }
                        >
                          {product.stock}
                        </span>
                      </td>
                      <td>
                        {providerNames.get(product.provider_id) ||
                          product.provider_id}
                      </td>
                      <td>
                        <div className="acciones-tabla">
                          <button
                            type="button"
                            onClick={() => openEditProduct(product)}
                          >
                            Editar
                          </button>
                          <button
                            className="accion-peligro"
                            type="button"
                            onClick={() => handleDeleteProduct(product)}
                          >
                            Desactivar
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {!products.length && (
                    <tr>
                      <td className="tabla-vacia" colSpan="7">
                        No hay productos para mostrar.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <section className="panel" id="marcas">
          <div className="panel-titulo">
            <div>
              <h2>Marcas</h2>
              <p>Crea o actualiza las marcas utilizadas por los productos.</p>
            </div>
          </div>

          <div className="marcas-layout">
            <form className="form-stack" onSubmit={handleBrandSubmit}>
              <label>
                Nombre de la marca
                <input
                  value={brandForm.name}
                  onChange={(event) =>
                    setBrandForm((current) => ({
                      ...current,
                      name: event.target.value,
                    }))
                  }
                  minLength="2"
                  maxLength="50"
                  required
                />
              </label>
              <label>
                Descripción
                <textarea
                  value={brandForm.description}
                  onChange={(event) =>
                    setBrandForm((current) => ({
                      ...current,
                      description: event.target.value,
                    }))
                  }
                  maxLength="100"
                  rows="3"
                  required
                />
              </label>
              <div className="acciones-form">
                <button className="boton-primario" type="submit" disabled={saving}>
                  {editingBrandId ? "Actualizar marca" : "Crear marca"}
                </button>
                {editingBrandId && (
                  <button
                    className="boton-secundario"
                    type="button"
                    onClick={() => {
                      setBrandForm(EMPTY_BRAND);
                      setEditingBrandId(null);
                    }}
                  >
                    Cancelar
                  </button>
                )}
              </div>
            </form>

            <div className="lista-marcas">
              {brands.map((brand) => (
                <article key={brand.id} className="marca-item">
                  <div>
                    <strong>{brand.name}</strong>
                    <p>{brand.description || "Sin descripción"}</p>
                  </div>
                  <div className="acciones-tabla">
                    <button type="button" onClick={() => editBrand(brand)}>
                      Editar
                    </button>
                    <button
                      className="accion-peligro"
                      type="button"
                      onClick={() => handleDeleteBrand(brand)}
                    >
                      Desactivar
                    </button>
                  </div>
                </article>
              ))}
              {!brands.length && (
                <p className="estado-carga">No hay marcas registradas.</p>
              )}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default Productos;
