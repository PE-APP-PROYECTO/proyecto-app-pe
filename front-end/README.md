# TECAPP Frontend

Frontend React conectado con la API FastAPI de TECAPP.

## Funciones conectadas

- Inicio de sesión OAuth2 mediante POST /api/v1/token.
- Registro público mediante POST /api/v1/usuarios/.
- Conservación opcional del JWT en localStorage; de lo contrario se usa
  sessionStorage.
- Envío automático de Authorization: Bearer TOKEN en las rutas protegidas.
- Cierre de sesión automático cuando la API responde 401.
- Lectura del rol incluido en el JWT: las pantallas de administración solo se
  muestran cuando `role` es `admin`.
- Íconos SVG propios para productos, proveedores y usuarios, sin emojis ni
  dependencias gráficas externas.
- Consulta, creación, edición y desactivación de productos y marcas.
- Consulta, creación, edición y desactivación de proveedores y usuarios.
- Búsqueda de productos desde la barra principal y filtros en las tablas.
- Asistente flotante conectado con POST /api/v1/chatbot/ para consultar el
  inventario real y el histórico de ventas de demostración.

## Configuración

1. Instala las dependencias:

       npm install

2. Crea el archivo de variables:

   En Windows PowerShell:

       Copy-Item .env.example .env

   En Linux o macOS:

       cp .env.example .env

3. Revisa la URL de la API en .env:

       VITE_API_URL=http://127.0.0.1:8000/api/v1

   Esta es la dirección original del backend local. Si el equipo backend cambia
   el puerto, actualiza únicamente este valor.

4. Inicia el frontend:

       npm run dev

## Inicio del backend

Desde la carpeta back-end, configura su .env, inicia PostgreSQL y ejecuta:

    uvicorn app.main:app --reload --port 8000

El login envía `username` y `password` como formulario OAuth2. La pantalla de
registro envía `fullName`, `email`, `document`, `password` y
`confirm_password` como JSON.

El asistente solo aparece después de iniciar sesión. La clave de Gemini se
configura exclusivamente en el `.env` del backend; nunca debe agregarse al
frontend ni a una variable que comience por `VITE_`.

Los usuarios sin rol `admin` pueden consultar desde Inicio los productos y las
marcas públicas, pero no acceden a proveedores, usuarios ni operaciones de
escritura.

## Observaciones del contrato actual

- En el OpenAPI publicado, POST /usuarios/ dejó de exigir OAuth2. Por eso el
  frontend ahora permite crear una cuenta desde el login.
- El backend debe responder 400 o 401 con un mensaje JSON cuando las credenciales
  sean incorrectas. Una respuesta 500 debe corregirse desde el backend.
- GET /usuarios/ incluye usuarios inactivos y UserResponseSchema no devuelve
  is_active. El frontend retira de la tabla al usuario recién desactivado, pero
  puede aparecer otra vez después de recargar. El backend debe exponer is_active
  o filtrar la lista para resolverlo de forma permanente.
- El backend usa ConflictError para registros duplicados y relaciones activas,
  pero no registra un manejador HTTP para esa excepción. Esos casos pueden
  responder 500 hasta que el backend registre ConflictError como respuesta 409.

## Verificación

    npm run lint
    npm run build

## Subir a GitHub

El proyecto ya incluye un `.gitignore` que excluye `node_modules`, `dist`,
archivos `.env` privados y configuraciones del editor. Desde la carpeta donde
está `package.json`, ejecuta:

    git init
    git add .
    git commit -m "Frontend TECAPP conectado con la API"
    git branch -M main
    git remote add origin URL_DE_TU_REPOSITORIO
    git push -u origin main

No subas un archivo `.env` real. GitHub debe contener únicamente
`.env.example`, porque la URL puede cambiar y ese archivo no guarda secretos.
