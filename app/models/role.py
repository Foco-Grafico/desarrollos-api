from pydantic import BaseModel

class CreateRole(BaseModel):
    name: str
    description: str
    permissions: list[str]
