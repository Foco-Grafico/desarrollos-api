from pydantic import BaseModel

class CreateSeller(BaseModel):
    name: str
    last_name: str
    email: str
    phone: str





