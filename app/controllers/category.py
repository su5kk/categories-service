"""Controller: read requests, call the model, and select a response view."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models import category as models
from app.views.category import CategoryView

router = APIRouter(prefix="/categories")


class CategoryBody(BaseModel):
    name: str
    countries: list[str]


def find_category_or_404(category_id: int):
    category = models.find_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch("/{category_id}", response_model=CategoryView, response_model_exclude_unset=True)
def update_category(category_id: int, body: CategoryBody):
    find_category_or_404(category_id)
    return models.update_category(category_id, body.name, body.countries)


@router.post("", response_model=CategoryView, response_model_exclude_unset=True)
def create_category(name: str):
    if models.name_exists(name):
        raise HTTPException(status_code=409, detail="Category name already exists")
    if not models.validate_name(name):
        raise HTTPException(status_code=400, detail="Category name is not valid")
    return models.create_category(name)


@router.get("", response_model=list[CategoryView], response_model_exclude_unset=True)
def list_categories():
    return models.list_categories()


@router.get("/{category_id}", response_model=CategoryView, response_model_exclude_unset=True)
def get_category(category_id: int):
    return find_category_or_404(category_id)


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int):
    find_category_or_404(category_id)
    models.delete_category(category_id)
