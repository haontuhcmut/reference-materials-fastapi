from pydantic import BaseModel, Field
import uuid

class CreateDhScheme(BaseModel):
    code: str = Field(default=None, max_length=15)
    sample_id: uuid.UUID | None = Field(default=None)
