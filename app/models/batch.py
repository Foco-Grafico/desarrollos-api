from pydantic import BaseModel
from fastapi import UploadFile, Form
from typing import Annotated

class FilterBatch(BaseModel):
    area: float | None = None
    perimeter: float | None = None
    longitude: float | None = None
    coords: str | None = None
    amenities: str | None = None
    price: float | None = None
    development_id: int | None = None
    currency: str | None = None
    location: str | None = None
    sq_m: float | None = None
    sides: int | None = None
    block: int | None = None
    type: int | None = None

class CreateBatch(BaseModel):
    block: int
    number_of_batch: int
    area: float
    perimeter: float
    longitude: float
    coords: str
    amenities: str
    price: float
    assets: list[UploadFile]
    development_id: int
    currency: str = 'MXN'
    location: str
    sq_m: float
    sides: int
    type: int

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
        development_id: Annotated[int, Form(...)],
        currency: Annotated[str, Form(...)],
        location: Annotated[str, Form(...)],
        sq_m: Annotated[float, Form(...)],
        sides: Annotated[int, Form(...)],
        block: Annotated[int, Form(...)],
        number_of_batch: Annotated[int, Form(...)],
        type: Annotated[int, Form(...)]
    ):
        return cls(
            area=area,
            perimeter=perimeter,
            longitude=longitude,
            coords=coords,
            amenities=amenities,
            price=price,
            assets=assets,
            development_id=development_id,
            currency=currency,
            location=location,
            sq_m=sq_m,
            sides=sides,
            block=block,
            number_of_batch=number_of_batch,
            type=type
        )

class EditBatch(BaseModel):
    area: float | None = None
    perimeter: float | None = None
    longitude: float | None = None
    coords: str | None = None
    amenities: str | None = None
    price: float | None = None
    development_id: int | None = None
    currency: str | None = None
    location: str | None = None
    sq_m: float | None = None
    sides: int | None = None
    block: int | None = None
    number_of_batch: int | None = None
    type: int | None = None

    @classmethod
    def as_form(
        cls,
        area: Annotated[float | None, Form(...)] = None,
        perimeter: Annotated[float | None, Form(...)] = None,
        longitude: Annotated[float | None, Form(...)] = None,
        coords: Annotated[str | None, Form(...)] = None,
        amenities: Annotated[str | None, Form(...)] = None,
        price: Annotated[float | None, Form(...)] = None,
        development_id: Annotated[int | None, Form(...)] = None,
        currency: Annotated[str | None, Form(...)] = None,
        location: Annotated[str | None, Form(...)] = None,
        sq_m: Annotated[float | None, Form(...)] = None,
        sides: Annotated[int | None, Form(...)] = None,
        block: Annotated[int | None, Form(...)] = None,
        number_of_batch: Annotated[int | None, Form(...)] = None,
        type: Annotated[int | None, Form(...)] = None
    ):
        return cls(
            area=area,
            perimeter=perimeter,
            longitude=longitude,
            coords=coords,
            amenities=amenities,
            price=price,
            development_id=development_id,
            currency=currency,
            location=location,
            sq_m=sq_m,
            sides=sides,
            block=block,
            number_of_batch=number_of_batch,
            type=type
        )