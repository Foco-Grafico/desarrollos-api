from pydantic import BaseModel
from fastapi import UploadFile, Form
from typing import Annotated

class CreateDevelopment(BaseModel):
    name: str
    description: str | None = None
    address: str
    city: str
    state: str
    country: str
    logo: UploadFile
    contact_number: str
    contact_email: str

    @classmethod
    def as_form(
        cls,
        name: Annotated[str, Form(...)],
        description: Annotated[str, Form(...)],
        address: Annotated[str, Form(...)],
        city: Annotated[str, Form(...)],
        state: Annotated[str, Form(...)],
        country: Annotated[str, Form(...)],
        logo: UploadFile,
        contact_number: Annotated[str, Form(...)],
        contact_email: Annotated[str, Form(...)]
    ):
        return cls(
            name=name,
            description=description,
            address=address,
            city=city,
            state=state,
            country=country,
            logo=logo,
            contact_number=contact_number,
            contact_email=contact_email
        )
