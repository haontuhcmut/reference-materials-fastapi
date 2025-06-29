from fastapi import APIRouter, UploadFile, File
from typing import Annotated
from app.sds.service import SDSService

sds_service = SDSService()
sds_route = APIRouter()


@sds_route.post("/uploadfile/")
async def upload_file(
    file: Annotated[UploadFile, File(description="Safety Data Sheet.pdf")],
):
    result = await sds_service.create_upload_file(file)
    return result
