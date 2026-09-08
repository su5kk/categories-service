"""Model: store categories and define the rules for working with them."""

import re

# ponytail: data resets on restart; use a database when persistence is needed.
categories = {
    1: {"id": 1, "name": "economy", "countries": ["ru, kz, gb"]},
    2: {"id": 2, "name": "comfort", "countries": ["kz"]},
    3: {"id": 3, "name": "comfort_plus", "countries": ["kz"]},
    4: {"id": 4, "name": "premium", "countries": ["us"]},
}


def find_category(category_id: int):
    return categories.get(category_id)


def list_categories():
    return list(categories.values())


def name_exists(name: str) -> bool:
    return any(category["name"] == name for category in categories.values())


def validate_name(name: str) -> bool:
    return re.search("^(?! )[a-z]+(?<! )$", name) is not None


def create_category(name: str):
    category_id = max(categories, default=0) + 1
    categories[category_id] = {"id": category_id, "name": name}
    return categories[category_id]


def update_category(category_id: int, name: str, countries: list[str]):
    category = categories[category_id]
    if name:
        category["name"] = name
    if countries:
        category["countries"] = countries
    return category


def delete_category(category_id: int):
    del categories[category_id]
