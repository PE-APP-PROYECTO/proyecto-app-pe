# 🚀 Nombre del Proyecto

Breve descripción de una o dos oraciones sobre lo que hace tu aplicación API y el problema que resuelve.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Framework:** FastAPI
* **Servidor ASGI:** Uvicorn
* **Base de Datos:** (ej. PostgreSQL / MongoDB / SQLite)
* **ORM:** (ej. SQLAlchemy / Tortoise-ORM / Motor)

---

## 📋 Prerrequisitos

Asegúrate de contar con lo siguiente instalado en tu entorno local:

* [Python 3.10+](https://www.python.org/)
* [Git](https://git-scm.com/)

---

## ⚙️ Configuración e Instalación

Sigue estos pasos para levantar el entorno de desarrollo local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/PE-APP-PROYECTO/proyecto-app-pe.git
cd proyecto-app-pe
```

### 2. Crear y activar el entorno virtual

Linux / macOS:

```bash
python -m venv venv
source venv/bin/activate
```

Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requerimientos.txt
```

### Configurar variables de entorno
crea un archivo .env en la raiz del proyecto basado en el archivo de ejemplo (.env.example)

```bash
cp .env.example .env
```
Define las variables necesarias en el archivo .env

### Ejecución del servidor
para iniciar el servidor en modo desarrollo con recarga automática:

```bash
uvicorn app.main:app --reload
python -m app.main
```


el servidor estará disponible en http://127.0.0.1:8000
                                 http:localhost:8000

## Documentación interactiva
FastAPI genera automáticamente la documentación interactiva OpenAPI:

- SWARGGET UI: http:localhost:8000/docs
- ReDoc: http:localhost:8000/redoc

## Estrutura del Proyecto

## Contribución

1. Haz un Fork del proyecto.

2. Crea una rama para tu función (git checkout -b feature/nueva-funcion).

3. Realiza tus commits (git commit -m 'Añade nueva función').

4. Haz Push a la rama (git push origin feature/nueva-funcion).

5. Abre un Pull Request.

## Configuración e Instalación del Entorno

Sigue estas instrucciones para levantar el contenedor de la base de datos PostgreSQL, ejecutar las migraciones del proyecto y transferir datos entre entornos.

1. Configuración de Variables de Entorno

Crea un archivo .env en la raíz del proyecto (back-end/) tomando como base el archivo .env.example:

```bash
# Copiar plantilla de entorno en Linux/macOS
cp .env.example .env

# Copiar plantilla de entorno en Windows (PowerShell)
Copy-Item .env.example -Destination .env
```
Asegúrate de definir las credenciales del servicio de base de datos dentro del archivo .env:
```bash
DB_USER_SECRET=
DB_PASSWORD_SECRET=
DB_HOST=
DB_PORT=
DB_NAME=
```
2. Despliegue del Contenedor de Base de Datos

Ejecuta el servicio de PostgreSQL desde la raíz del proyecto (back-end/) haciendo referencia a la ubicación del archivo Compose:

```bash
# Iniciar contenedor en Linux (usando Docker o Podman)
docker compose -f app/db/docker-compose.yml up -d

# Iniciar contenedor en Windows (PowerShell / CMD)
docker compose -f app/db/docker-compose.yml up -d
o
docker compose --env-file ..\.env up -d
```
3. Gestión de Migraciones con Alembic

Todas las migraciones deben ejecutarse desde la raíz del proyecto (back-end/).

    Generar una nueva migración (después de modificar o crear modelos en SQLAlchemy):

```bash
alembic revision --autogenerate -m "descripcion de los cambios"
```

    Aplicar las migraciones en la base de datos:
```bash
alembic upgrade head
```
4. Migración de Datos Entre Equipos (Respaldos)

Las migraciones de Alembic aplican únicamente cambios en la estructura del esquema (tablas y columnas), no en los datos guardados. Para trasladar registros entre máquinas, exporta e importa un respaldo de PostgreSQL.

Exportar datos (PC de Origen):

    Linux / macOS:
```bash
docker exec -t dbTecApp pg_dump -U wilmarito -d dbTecApp > respaldo.sql
```
    Windows (PowerShell):
```bash
docker exec -t dbTecApp pg_dump -U wilmarito -d dbTecApp | Out-File -Encoding utf8 respaldo.sql
```
Importar datos (PC de Destino):

    Linux / macOS:
```bash
cat respaldo.sql | docker exec -i dbTecApp psql -U wilmarito -d dbTecApp
```

    Windows (PowerShell):
```bash
Get-Content respaldo.sql | docker exec -i dbTecApp psql -U wilmarito -d dbTecApp
```
