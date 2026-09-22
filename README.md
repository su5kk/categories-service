# Taxi categories: MVC with FastAPI

MVC splits the app into three responsibilities:

| Layer | File | Responsibility |
| --- | --- | --- |
| Model | `app/models/category.py` | Store categories, read and change data, define name rules. |
| View | `app/views/category.py` | Describe the category fields sent to the client as JSON. |
| Controller | `app/controllers/category.py` | Handle HTTP requests, call model functions, choose the response schema and HTTP errors. |

`app/main.py` creates the FastAPI app and connects its routes.

## Project structure

```text
app/
├── __init__.py
├── main.py
├── models/
│   ├── __init__.py
│   └── category.py
├── views/
│   ├── __init__.py
│   └── category.py
└── controllers/
    ├── __init__.py
    └── category.py
requirements.txt
README.md
```

Each Python file is a module. A folder with an `__init__.py` file is a package; these files can stay empty. Imports such as `from app.views.category import CategoryView` show which layer owns the code.

## Follow a request

For `GET /categories/1`:

1. FastAPI calls `get_category()` in `app/controllers/category.py`.
2. The controller asks `models.find_category(1)` for the category.
3. The model queries SQLite using SQLAlchemy Core and returns the data.
4. The controller returns that data. FastAPI uses `CategoryView` from `app/views/category.py` to validate and serialize the JSON response.

If the model returns `None`, the controller sends an HTTP 404 error. The model does not need to know what HTTP is.

This API uses JSON as its view. In a website that renders HTML, templates would fill that role. The `CategoryBody` class in the controller describes incoming data; `CategoryView` describes outgoing data.

## Run

Use Python 3.10 or newer, from this directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the routes.

Or start it with Docker Compose:

```sh
docker-compose up --build
```

When run directly, categories persist in `categories.db` in the project directory. On first startup,
the app creates the table and inserts the four sample categories. Later restarts
keep your changes, including deletions. Countries are stored as a JSON list.
Writes use [SQLAlchemy transactions](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html).
Table creation does not migrate an existing schema; add migrations when the schema changes.

| Method | Path | Input |
| --- | --- | --- |
| GET | `/categories` | None |
| GET | `/categories/{category_id}` | Category ID |
| POST | `/categories?name=business` | Name in the query string |
| PATCH | `/categories/{category_id}` | JSON with `name` and `countries` |
| DELETE | `/categories/{category_id}` | Category ID |
