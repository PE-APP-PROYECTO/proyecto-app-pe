import { IconoModulo } from "./IconosSistema";

function TarjetaProducto({
  marca,
  nombre,
  descripcion,
  precio,
  stock,
  onView,
}) {
  return (
    <div className="tarjeta-producto">
      <div className="imagen-producto">
        <IconoModulo tipo="productos" size={92} />
      </div>
      <span className="marca-producto">{marca}</span>
      <h3>{nombre}</h3>
      <p>{descripcion}</p>
      <strong>{precio}</strong>
      {stock !== undefined && (
        <small className="stock-producto">Disponibles: {stock}</small>
      )}
      {onView && (
        <button type="button" onClick={onView}>
          Ver en inventario
        </button>
      )}
    </div>
  );
}

export default TarjetaProducto;
