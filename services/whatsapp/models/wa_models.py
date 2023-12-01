from pydantic import BaseModel
from enum import Enum

class Interactive(BaseModel):
    id: str
    title: str

class Image(BaseModel):
    mime_type: str
    id: str
    sha256: str

class MsgUser(BaseModel):
    number: str
    name: str

class Msg(BaseModel):
    id: str
    type: str
    message: str | Interactive | Image
    user: MsgUser

class Button(BaseModel):
    execute: str
    title: str

class HeaderTypes(Enum):
    document = 'document'
    image = 'image'
    text = 'text'

class Header():
    def __init__(
        self,
        type: HeaderTypes,
        text: str | None = None,
        url: str | None = None,
        preview_url: bool = True,
        filename: str | None = None,
    ) -> None:
        self.type = type
        self.text = text
        self.url = url
        self.preview_url = preview_url
        self.filename = filename
        pass

    def get(self):
        body = {
            'type': self.type.value
        }

        if self.type == HeaderTypes.text:
            body['text'] = self.text # type: ignore
            return body
        
        if self.type == HeaderTypes.image:
            body[self.type.value] = { # type: ignore
                'link': self.url
            }

            return body
        

        if self.type == HeaderTypes.document:
            body[self.type.value] = { # type: ignore
                'link': self.url,
                'filename': self.filename
            }

            if self.text:
                body[self.type.value]['caption'] = self.text # type: ignore

        return body

class Buttons():
    def __init__(
        self,
        body: str,
        buttons: list[Button],
        header: Header | None = None,
        footer: str | None = None,
    ) -> None:
        self.header = header
        self.body = body
        self.footer = footer
        self.buttons = buttons
        pass

    def get(self, to: str):
        body = {
            'to': to,
            'type': 'interactive',
            'interactive': {
                'type': 'button',
                'body': {
                    'text': self.body
                },
                'action': {
                    'buttons': [
                        {
                            'type': 'reply',
                            'reply': {
                                'id': button.execute.lower(),
                                'title': button.title
                            }
                        } for button in self.buttons
                    ]
                }

            },
            'recipient_type': 'individual',
            'messaging_product': 'whatsapp'
        }

        if self.header:
            body['interactive']['header'] = self.header.get()

        if self.footer:
            body['interactive']['footer'] = {
                'text': self.footer
            }

        return body
    
class ListElement(BaseModel):
    execute: str
    title: str
    description: str | None = None

class SectionList(BaseModel):
    title: str
    rows: list[ListElement]

class List():
    def __init__(
        self,
        body: str,
        button: str,
        sections: list[SectionList],
        header: Header | None = None,
        footer: str | None = None,
    ) -> None:
        self.header = header
        self.body = body
        self.footer = footer
        self.button = button
        self.sections = sections
        pass

    def get(self, to: str):
        body = {
            'to': to,
            'type': 'interactive',
            'interactive': {
                'type': 'list',
                'body': {
                    'text': self.body
                },
                'action': {
                    'button': self.button,
                    'sections': [
                        {
                            'title': section.title,
                            'rows': [
                                {
                                    'id': row.execute.lower(),
                                    'title': row.title,
                                    'description': row.description
                                } for row in section.rows
                            ]
                        } for section in self.sections
                    ]
                }
            },
            'recipient_type': 'individual',
            'messaging_product': 'whatsapp'
        }

        if self.header:
            body['interactive']['header'] = self.header.get()

        if self.footer:
            body['interactive']['footer'] = {
                'text': self.footer
            }

        return body