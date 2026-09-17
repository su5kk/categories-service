"""Model: store categories and define the rules for working with them."""

import re
from pathlib import Path

from sqlalchemy import (
    JSON, Column, Integer, MetaData, String, Table, create_engine, inspect, select,
)

database_path = Path(__file__).resolve().parents[2] / "categories.db"
engine = create_engine(f"sqlite:///{database_path}")

metadata = MetaData()
categories = Table(
    "categories",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("countries", JSON, nullable=True),
)


def initialize_database():
    with engine.begin() as connection:
        if inspect(connection).has_table("categories"):
            return

        metadata.create_all(connection)
        sample_categories = [
            {"id": 1, "name": "economy", "countries": ["ru, kz, gb"]},
            {"id": 2, "name": "comfort", "countries": ["kz"]},
            {"id": 3, "name": "comfort_plus", "countries": ["kz"]},
            {"id": 4, "name": "premium", "countries": ["us"]},
        ]
        connection.execute(categories.insert(), sample_categories)


def find_category(category_id: int):
    # .c gives access to table columns. This builds SQL without executing it.
    query = select(categories).where(categories.c.id == category_id)
    with engine.connect() as connection:
        # mappings() makes rows accessible by column name; first() may be None.
        row = connection.execute(query).mappings().first()
        if row is None:
            return None
        return dict(row)


def list_categories():
    query = select(categories).order_by(categories.c.id)
    with engine.connect() as connection:
        rows = connection.execute(query).mappings()
        return [dict(row) for row in rows]


def name_exists(name: str) -> bool:
    query = select(categories.c.id).where(categories.c.name == name).limit(1)
    with engine.connect() as connection:
        category_id = connection.scalar(query)
        return category_id is not None


def validate_name(name: str) -> bool:
    return re.search("^(?! )[a-z]+(?<! )$", name) is not None


def create_category(name: str):
    query = categories.insert().values(name=name)
    with engine.begin() as connection:
        result = connection.execute(query)
        category_id = result.inserted_primary_key[0]
        return {"id": category_id, "name": name, "countries": None}


def update_category(category_id: int, name: str, countries: list[str]):
    # Empty inputs leave the existing values unchanged.
    values = {}
    if name:
        values["name"] = name
    if countries:
        values["countries"] = countries
    with engine.begin() as connection:
        if values:
            query = categories.update().where(categories.c.id == category_id).values(values)
            connection.execute(query)
        query = select(categories).where(categories.c.id == category_id)
        row = connection.execute(query).mappings().one()
        return dict(row)


def delete_category(category_id: int):
    query = categories.delete().where(categories.c.id == category_id)
    with engine.begin() as connection:
        connection.execute(query)
