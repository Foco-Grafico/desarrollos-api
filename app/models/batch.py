from pydantic import BaseModel
from fastapi import UploadFile, Form
from typing import Annotated

class PaymentPlan(BaseModel):
    price: float
    months_to_pay: int
    annuity: float
    pay_per_month: float
    interest_rate: float
    payment_method: str

class CreateBatch(BaseModel):
    area: str
    perimeter: str
    longitude: str
    coords: str
    amenities: str
    price: float
    assets: list[UploadFile]

    @classmethod
    def as_form(
        cls,
        area: Annotated[str, Form(...)],
        perimeter: Annotated[str, Form(...)],
        longitude: Annotated[str, Form(...)],
        coords: Annotated[str, Form(...)],
        amenities: Annotated[str, Form(...)],
        price: Annotated[float, Form(...)],
        assets: list[UploadFile]
    ):
        return cls(
            area=area,
            perimeter=perimeter,
            longitude=longitude,
            coords=coords,
            amenities=amenities,
            price=price,
            assets=assets
        )