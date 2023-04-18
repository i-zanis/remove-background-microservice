import shutil
import subprocess
import tempfile
from pathlib import Path

from fastapi import UploadFile


async def remove_background(file: UploadFile):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) \
                as temp_file:
            temp_path = Path(temp_file.name)
            shutil.copyfileobj(file.file, temp_file)

        process = subprocess.run(["rembg", "i", str(temp_path)],
                                 capture_output=True)

        has_processed_failed = process.returncode != 0
        if has_processed_failed:
            return {"success": False}

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") \
                as output_temp_file:
            output_temp_file.write(process.stdout)

        return {"success": True, "file_path": output_temp_file.name}

    except Exception as e:
        print(f"Error in remove_background: {e}")
        return {"success": False}
