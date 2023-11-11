from pydantic import BaseModel
from typing import Annotated
from fastapi import Form

class CreateSeller(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    enterprise: str | None = None

    @classmethod
    def as_form(
        cls,
        first_name: Annotated[str, Form(...)],
        last_name: Annotated[str, Form(...)],
        email: Annotated[str, Form(...)],
        phone_number: Annotated[str, Form(...)],
        enterprise: Annotated[str | None, Form(...)] = None,
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            enterprise=enterprise
    )

class EditSeller(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    enterprise: str | None = None

    @classmethod
    def as_form(
        cls,
        first_name: Annotated[str | None, Form(...)] = None,
        last_name: Annotated[str | None, Form(...)] = None,
        email: Annotated[str | None, Form(...)] = None,
        phone_number: Annotated[str | None, Form(...)] = None,
        enterprise: Annotated[str | None, Form(...)] = None,
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            enterprise=enterprise
    )




