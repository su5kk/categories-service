"""View: describe the JSON that clients receive, instead of HTML pages."""

from pydantic import BaseModel


class CategoryView(BaseModel):
    id: int
    name: str
    countries: list[str] | None = None
