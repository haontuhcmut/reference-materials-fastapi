from pathlib import Path
from fastapi import UploadFile, File
from typing import Annotated
import aiofiles
from app.error import InvalidFileExtension

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / ("sds_storage")
UPLOAD_DIR.mkdir(exist_ok=True)

class SDSService:
    async def create_upload_file(
        self,
        file: Annotated[UploadFile, File(description="Safety Data Sheet.pdf")],
    ):
        """Upload a file and save in local storage"""
        if not file.content_type.endswith("application/pdf"):
            raise InvalidFileExtension()
        headers = await file.read(5)
        if headers != b"%PDF-":
            raise InvalidFileExtension()
        
        file_path = UPLOAD_DIR / file.filename
        async with aiofiles.open(file_path, "wb") as new_file:
            contents = await file.read()
            await new_file.write(contents)
        return {"file_name": file.filename, "status": "success"}
    