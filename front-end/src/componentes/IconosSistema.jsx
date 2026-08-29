export function IconoModulo({ tipo, size = 48, className = "" }) {
  const commonProps = {
    width: size,
    height: size,
    viewBox: "0 0 64 64",
    fill: "none",
    xmlns: "http://www.w3.org/2000/svg",
    className,
    "aria-hidden": true,
  };

  if (tipo === "proveedores") {
    return (
      <svg {...commonProps}>
        <path
          d="M7 17.5h29v28H7v-28Z"
          fill="#DBEAFE"
          stroke="#1D4ED8"
          strokeWidth="3"
          strokeLinejoin="round"
        />
        <path
          d="M36 27h10.5L57 37.5v8H36V27Z"
          fill="#EFF6FF"
          stroke="#1D4ED8"
          strokeWidth="3"
          strokeLinejoin="round"
        />
        <path d="M42 28v10h13" stroke="#1D4ED8" strokeWidth="3" />
        <circle cx="18" cy="47" r="6" fill="#172554" stroke="white" strokeWidth="3" />
        <circle cx="47" cy="47" r="6" fill="#172554" stroke="white" strokeWidth="3" />
        <path d="M14 25h15M14 32h10" stroke="#2563EB" strokeWidth="3" strokeLinecap="round" />
      </svg>
    );
  }

  if (tipo === "usuarios") {
    return (
      <svg {...commonProps}>
        <circle cx="24" cy="23" r="9" fill="#DBEAFE" stroke="#1D4ED8" strokeWidth="3" />
        <circle cx="45" cy="25" r="7" fill="#EFF6FF" stroke="#1D4ED8" strokeWidth="3" />
        <path
          d="M8 52c0-10 7-16 16-16s16 6 16 16H8Z"
          fill="#DBEAFE"
          stroke="#1D4ED8"
          strokeWidth="3"
          strokeLinejoin="round"
        />
        <path
          d="M38 39c2-2 4.5-3 7.5-3 6.5 0 11.5 5 11.5 13H41"
          fill="#EFF6FF"
          stroke="#1D4ED8"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    );
  }

  return (
    <svg {...commonProps}>
      <rect x="15" y="6" width="34" height="52" rx="7" fill="#172554" />
      <rect x="19" y="12" width="26" height="37" rx="3" fill="#EFF6FF" />
      <rect x="22" y="17" width="20" height="6" rx="2" fill="#2563EB" />
      <rect x="22" y="27" width="8" height="8" rx="2" fill="#93C5FD" />
      <rect x="34" y="27" width="8" height="8" rx="2" fill="#BFDBFE" />
      <path d="M22 40h20" stroke="#60A5FA" strokeWidth="3" strokeLinecap="round" />
      <circle cx="32" cy="53" r="2" fill="white" />
    </svg>
  );
}

export function IlustracionInventario() {
  return (
    <svg
      className="hero-illustration"
      viewBox="0 0 430 310"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="Panel digital de gestión de inventario"
    >
      <circle cx="220" cy="155" r="132" fill="#FFFFFF" fillOpacity="0.08" />
      <circle cx="220" cy="155" r="98" fill="#FFFFFF" fillOpacity="0.06" />

      <g transform="translate(115 24)">
        <rect x="0" y="0" width="200" height="262" rx="28" fill="#0B1739" />
        <rect x="10" y="11" width="180" height="239" rx="21" fill="#F8FAFC" />
        <rect x="70" y="6" width="60" height="8" rx="4" fill="#0B1739" />
        <rect x="27" y="31" width="146" height="36" rx="10" fill="#1D4ED8" />
        <circle cx="45" cy="49" r="7" fill="#BFDBFE" />
        <rect x="59" y="42" width="50" height="5" rx="2.5" fill="white" />
        <rect x="59" y="52" width="34" height="4" rx="2" fill="#BFDBFE" />

        <rect x="27" y="82" width="68" height="68" rx="12" fill="#E0ECFF" />
        <rect x="105" y="82" width="68" height="68" rx="12" fill="#EEF2FF" />
        <path d="M42 130V108l13 8 13-18 13 11" fill="none" stroke="#2563EB" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" />
        <rect x="119" y="100" width="39" height="8" rx="4" fill="#60A5FA" />
        <rect x="119" y="115" width="28" height="7" rx="3.5" fill="#93C5FD" />
        <rect x="119" y="129" width="36" height="7" rx="3.5" fill="#BFDBFE" />

        <rect x="27" y="164" width="146" height="60" rx="12" fill="white" stroke="#D8E3F4" strokeWidth="2" />
        <rect x="40" y="178" width="33" height="33" rx="8" fill="#DBEAFE" />
        <path d="M48 188h17v13H48zM52 184h9v4h-9z" fill="#2563EB" />
        <rect x="84" y="179" width="66" height="7" rx="3.5" fill="#1E3A8A" />
        <rect x="84" y="193" width="49" height="6" rx="3" fill="#93A4BD" />
        <rect x="84" y="205" width="35" height="6" rx="3" fill="#BFDBFE" />
      </g>

      <g transform="translate(39 177)">
        <rect x="0" y="18" width="83" height="66" rx="12" fill="#FFFFFF" />
        <path d="M0 37 41 15l42 22-42 22L0 37Z" fill="#93C5FD" />
        <path d="M0 37v42l41 22V59L0 37Z" fill="#DBEAFE" />
        <path d="M83 37v42l-42 22V59l42-22Z" fill="#BFDBFE" />
        <path d="m25 24 42 22" stroke="#2563EB" strokeWidth="4" />
      </g>

      <g transform="translate(316 74)">
        <rect width="85" height="74" rx="15" fill="#FFFFFF" />
        <circle cx="24" cy="25" r="9" fill="#DBEAFE" />
        <path d="M20 25h8M24 21v8" stroke="#1D4ED8" strokeWidth="3" strokeLinecap="round" />
        <rect x="40" y="20" width="29" height="7" rx="3.5" fill="#1E3A8A" />
        <rect x="16" y="46" width="53" height="8" rx="4" fill="#BFDBFE" />
      </g>
    </svg>
  );
}
