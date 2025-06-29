import os
from fastapi import UploadFile, File
from typing import Annotated


class SDSService:
    async def create_upload_file(
        self,
        file: Annotated[UploadFile, File(description="Safety Data Sheet.pdf")],
    ):
        
        pass
k