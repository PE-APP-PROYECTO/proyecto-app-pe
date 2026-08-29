import { IconoModulo } from "./IconosSistema";

function TarjetaCategoria({ tipoIcono, titulo, descripcion }) {
  return (
    <div className="tarjeta-categoria">
      <div className="icono-categoria">
        <IconoModulo tipo={tipoIcono} size={58} />
      </div>
      <h3>{titulo}</h3>
      <p>{descripcion}</p>
    </div>
  );
}

export default TarjetaCategoria;
