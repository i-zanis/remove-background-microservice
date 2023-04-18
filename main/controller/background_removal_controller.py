from fastapi import APIRouter, File, UploadFile, Response
from fastapi.responses import FileResponse

from service.background_removal_service import remove_background

router = APIRouter()


@router.post("/remove-background", response_class=FileResponse, responses={
    200: {"description": "Background removed successfully"},
    500: {"description": "Error in removing background"}
})
async def remove_background_route(file: UploadFile = File(...)):
    result = await remove_background(file)
    if result["success"]:
        return FileResponse(
            result["file_path"],
            media_type="image/png",
            headers={
                "Content-Disposition": "attachment;filename=processed_image.png"
            }
        )
    return Response(content="Error in removing background", status_code=500)
