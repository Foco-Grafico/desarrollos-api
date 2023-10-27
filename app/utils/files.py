from fastapi import UploadFile
from os import path as os_path
from uuid import uuid4 as v4

def is_image(file: UploadFile):
    if not file.filename:
        return False

    extension_file = file.filename.split('.')[-1]

    if extension_file.lower() not in ['png', 'jpg', 'jpeg', 'svg', 'webp']:
        return False

    return True

def save_file_on_api(file: UploadFile, path: str):
    constructed_path = os_path.join(path, f'{v4()}-{file.filename}')

    with open(constructed_path, 'wb') as buffer:
        buffer.write(file.file.read())
        buffer.close()

    return constructed_path.replace('\\', '/')