import shutil
import tempfile
from pathlib import Path

from fastapi import UploadFile
from rembg import remove


async def remove_background(file: UploadFile):
    try:
        temp_path = await create_temp_input_file(file)
        input_data = await read_input_file(temp_path)
        output_data = remove(input_data)
        if output_data is None:
            return {"success": False}
        output_file_path = await create_temp_output_file(output_data)
        return {"success": True, "file_path": output_file_path}

    except (Exception) as e:
        return {"success": False, "error": str(e)}


async def create_temp_input_file(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False,
                                     suffix=file.filename) as temp_file:
        temp_path = Path(temp_file.name)
        shutil.copyfileobj(file.file, temp_file)
    return temp_path


async def read_input_file(temp_path: Path):
    with open(temp_path, 'rb') as input_file:
        input_data = input_file.read()
    return input_data


async def create_temp_output_file(output_data: bytes):
    with tempfile.NamedTemporaryFile(delete=False,
                                     suffix=".png") as output_temp_file:
        output_temp_file.write(output_data)
    return output_temp_file.name
