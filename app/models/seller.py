from pydantic import BaseModel

class CreateSeller(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    enterprise: str | None = None





