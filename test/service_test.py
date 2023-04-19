import pytest
from fastapi import UploadFile

from main.service.background_removal_service import remove_background


@pytest.fixture(scope="module")
def test_image():
    with open("test_image.png", "rb") as f:
        yield UploadFile(f)


async def test_remove_background_success(test_image):
    result = await remove_background(test_image)
    assert result["success"] == True
    assert "file_path" in result


async def test_remove_background_failure(test_image):
    with open("test_image.txt", "rb") as f:
        wrong_file = UploadFile(f)
        result = await remove_background(wrong_file)
        assert result["success"] == False


async def test_remove_background_exception(test_image, monkeypatch):
    def raise_error(*args, **kwargs):
        raise Exception("Test Exception")

    monkeypatch.setattr("subprocess.run", raise_error)
    result = await remove_background(test_image)
    assert result["success"] == False
