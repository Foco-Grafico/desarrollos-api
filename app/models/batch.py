from pydantic import BaseModel
from fastapi import UploadFile, Form
from typing import Annotated

class CreateBatch(BaseModel):
    area: float
    perimeter: float
    longitude: float
    coords: str
    amenities: str
    price: float
    assets: list[UploadFile]
    development_id: int

    @classmethod
    def as_form(
        cls,
        area: Annotated[float, Form(...)],
        perimeter: Annotated[float, Form(...)],
        longitude: Annotated[float, Form(...)],
        coords: Annotated[str, Form(...)],
        amenities: Annotated[str, Form(...)],
        price: Annotated[float, Form(...)],
        assets: list[UploadFile],
        development_id: Annotated[int, Form(...)]
    ):
        return cls(
            area=area,
            perimeter=perimeter,
            longitude=longitude,
            coords=coords,
            amenities=amenities,
            price=price,
            assets=assets,
            development_id=development_id
        )