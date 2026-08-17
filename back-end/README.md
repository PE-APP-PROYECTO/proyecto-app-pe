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
