from fastapi import UploadFile
from os import path as os_path, sep as os_sep, remove as os_remove
from uuid import uuid4 as v4

def delete_file(path: str):
    if os_path.exists(path):
        os_remove(path)

def is_image(file: UploadFile):
    if not file.filename:
        return False

    extension_file = file.filename.split('.')[-1]

    if extension_file.lower() not in ['png', 'jpg', 'jpeg', 'svg', 'webp']:
        return False
    
    if not file.content_type:
        return False

    if not file.content_type.lower().startswith('image'):
        return False

    return True

def save_file_on_api(file: UploadFile, path: str, exact_path: bool = False):
    if not file.filename:
        raise Exception('File name is required')
    

    if exact_path:
        delete_file(path)
        extension_file = file.filename.split('.')[-1]
        constructed_path = path.split('.')[0] + '.' + extension_file
    else:
        constructed_path = os_path.join(path, f'{v4()}-{file.filename}')

    with open(constructed_path, 'wb') as buffer:
        buffer.write(file.file.read())
        buffer.close()

    return constructed_path.replace(os_sep, '/')