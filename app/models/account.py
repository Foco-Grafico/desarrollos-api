from pydantic import BaseModel

class AccountCreate(BaseModel):
    name: str
    email: str
    password: str