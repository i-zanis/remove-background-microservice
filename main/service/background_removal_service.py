import shutil
import tempfile
from pathlib import Path

from fastapi import UploadFile
from rembg import remove


async def remove_background(file: UploadFile):
    try:
        temp_path = await _create_temp_input_file(file)
        input_data = await _read_input_file(temp_path)
        output_data = remove(input_data)
        if output_data is None:
            return await _handle_no_output()
        output_file_path = await _create_temp_output_file(output_data)
        return await _handle_success(output_file_path)

    except Exception as e:
        return await _handle_error(e)


async def _handle_error(e):
    return {"success": False, "error": str(e)}


async def _handle_success(output_file_path):
    return {"success": True, "file_path": output_file_path}


async def _create_temp_input_file(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False,
                                     suffix=file.filename) as temp_file:
        temp_path = Path(temp_file.name)
        shutil.copyfileobj(file.file, temp_file)
    return temp_path


async def _read_input_file(temp_path: Path):
    with open(temp_path, 'rb') as input_file:
        input_data = input_file.read()
    return input_data


async def _create_temp_output_file(output_data: bytes):
    with tempfile.NamedTemporaryFile(delete=False,
                                     suffix=".png") as output_temp_file:
        output_temp_file.write(output_data)
    return output_temp_file.name


async def _handle_no_output():
    return {"success": False, "error": "Output data is None"}
