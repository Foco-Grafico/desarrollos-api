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
    view_url: str | None = None
    max_blocks: int
    slug: str

    @classmethod
    def as_form(
        cls,
        name: Annotated[str, Form(...)],
        address: Annotated[str, Form(...)],
        city: Annotated[str, Form(...)],
        state: Annotated[str, Form(...)],
        country: Annotated[str, Form(...)],
        logo: UploadFile,
        contact_number: Annotated[str, Form(...)],
        contact_email: Annotated[str, Form(...)],
        max_blocks: Annotated[int, Form(...)],
        slug: Annotated[str, Form(...)],
        description: Annotated[str | None, Form(...)] = None,
        view_url: Annotated[str | None, Form(...)] = None
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
            contact_email=contact_email,
            view_url=view_url,
            max_blocks=max_blocks,
            slug=slug
        )

class EditDevelopment(BaseModel):
    name: str | None = None
    description: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    logo: UploadFile | None = None
    contact_number: str | None = None
    contact_email: str | None = None
    max_blocks: int | None = None
    slug: str | None = None
    view_url: str | None = None

    @classmethod
    def as_form(
        cls,
        name: Annotated[str | None, Form(...)] = None,
        description: Annotated[str | None, Form(...)] = None,
        address: Annotated[str | None, Form(...)] = None,
        city: Annotated[str | None, Form(...)] = None,
        state: Annotated[str | None, Form(...)] = None,
        country: Annotated[str | None, Form(...)] = None,
        logo: UploadFile | None = None,
        contact_number: Annotated[str | None, Form(...)] = None,
        contact_email: Annotated[str | None, Form(...)] = None,
        max_blocks: Annotated[int | None, Form(...)] = None,
        slug: Annotated[str | None, Form(...)] = None,
        view_url: Annotated[str | None, Form(...)] = None
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
            contact_email=contact_email,
            max_blocks=max_blocks,
            slug=slug,
            view_url=view_url
        )
