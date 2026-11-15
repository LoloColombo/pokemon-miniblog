# Pokémon Mini Blog — FastAPI

API REST de un blog sobre el mundo Pokémon. Proyecto de la materia Desarrollo de Sistemas Web (3° año), basado en el Mini Blog visto en clase ([cgldev/fastapi-miniblog](https://github.com/cgldev/fastapi-miniblog)).

## Temática

- **Posts**: entradas sobre Pokémon (fichas, guías, estrategias).
- **Categorías**: los tipos Pokémon (Fuego, Agua, Planta, Eléctrico, Psíquico…). Un post pertenece a una sola categoría.
- **Tags**: etiquetas libres como región o característica (`kanto`, `johto`, `legendario`, `competitivo`…). Un post puede tener varias.
- **Usuarios**: entrenadores con roles `user`, `editor` y `admin`.

## Funcionalidades

- CRUD de posts con búsqueda, paginación, orden, filtro por tags e imagen opcional.
- Slug automático y único para cada post, y consulta por slug.
- Usuarios reales en base de datos, contraseñas cifradas con pwdlib (Argon2) y login con JWT.
- Roles: `user` lee contenido, `editor` crea y edita posts, tags y categorías, `admin` gestiona usuarios y borra categorías.
- CRUD de tags con paginación y endpoint de la etiqueta más usada.
- CRUD de categorías con slug.
- Seeds para cargar datos iniciales con un comando.

## Tecnologías

Python, FastAPI, Pydantic v2, SQLAlchemy 2, SQLite (local) / PostgreSQL, PyJWT, pwdlib, python-slugify, Typer.

## Estructura

```text
app/
├── main.py
├── core/          db.py, security.py
├── models/        user.py, category.py, tag.py, post.py
├── services/      pagination.py, file_storage.py
├── utils/         slugify_utils.py
├── seeds/         data.py, service.py, run.py
└── api/v1/
    ├── auth/
    ├── users/
    ├── posts/
    ├── tags/
    ├── categories/
    └── uploads/
```

## Instalación en Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Si ya tenías un `blog.db` de una versión anterior, borralo antes de seguir: el esquema cambió.

## Cargar datos iniciales

```powershell
python -m app.seeds all
```

También se pueden cargar por partes: `users`, `categories`, `tags`, `posts`.

Usuarios de prueba (contraseña `pokemon123`, configurable con `SEED_PASSWORD`):

| Usuario | Email | Rol |
|---|---|---|
| profesor-oak | oak@pokeblog.com | admin |
| misty | misty@pokeblog.com | editor |
| brock | brock@pokeblog.com | editor |
| ash | ash@pokeblog.com | user |

## Ejecutar la API

```powershell
fastapi dev app/main.py
```

Documentación interactiva: `http://127.0.0.1:8000/docs`. Para probar endpoints protegidos, usar el botón **Authorize** con el email o el usuario y la contraseña.

## Endpoints

Todos bajo `/api/v1`.

| Método | Ruta | Acceso |
|---|---|---|
| `POST` | `/auth/register` | Público |
| `POST` | `/auth/login` | Público |
| `GET` | `/auth/me` | Autenticado |
| `GET` | `/users` | Admin |
| `GET` | `/users/{id}` | Admin |
| `PATCH` | `/users/{id}/role` | Admin |
| `PATCH` | `/users/{id}/active` | Admin |
| `DELETE` | `/users/{id}` | Admin |
| `GET` | `/posts` | Público |
| `GET` | `/posts/by-tags` | Público |
| `GET` | `/posts/post/{slug}` | Público |
| `GET` | `/posts/{id}` | Público |
| `POST` | `/posts` | Editor |
| `PUT` | `/posts/{id}` | Editor |
| `DELETE` | `/posts/{id}` | Editor |
| `GET` | `/tags` | Público |
| `GET` | `/tags/popular` | Público |
| `GET` | `/tags/{id}` | Público |
| `POST` | `/tags` | Editor |
| `PUT` | `/tags/{id}` | Editor |
| `DELETE` | `/tags/{id}` | Editor |
| `GET` | `/categories` | Público |
| `GET` | `/categories/slug/{slug}` | Público |
| `GET` | `/categories/{id}` | Público |
| `POST` | `/categories` | Editor |
| `PUT` | `/categories/{id}` | Editor |
| `DELETE` | `/categories/{id}` | Admin |
| `POST` | `/upload/save` | Público |

## Variables de entorno

| Variable | Uso |
|---|---|
| `DATABASE_URL` | Conexión a la base. Por defecto SQLite local |
| `SECRET_KEY` | Secreto para firmar los JWT. Obligatorio cambiarlo en producción |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token |
| `SEED_PASSWORD` | Contraseña de los usuarios del seed |

No subir el archivo `.env` a GitHub.

## Autor

Lorenzo Colombo — [@LoloColombo](https://github.com/LoloColombo). Base del proyecto: César Gimenez Lascano — [@cgldev](https://github.com/cgldev).
