from pydantic import BaseModel

class CreateBatch(BaseModel):
    area: str
    perimeter: str
    longitude: str
    coords: str
    amenities: str
    payment_plans: list[int]
    price: float