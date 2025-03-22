from fastapi import APIRouter, HTTPException, status
from app.db.models import Sample
from app.db.dependencies import SessionDep
from app.sample.services import SampleServices
from app.sample.schemas import CreateSampleScheme


sample_service = SampleServices()
sample_route = APIRouter()

@sample_route.get("/", response_model=list[Sample])
async def get_samples(session: SessionDep):
    samples = await sample_service.get_samples(session)
    return samples

@sample_route.get("/{sample_item}", response_model=Sample)
async def get_sample_item(sample_item: str, session:SessionDep):
    sample = await sample_service.get_sample_item(sample_item, session)
    if sample is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    return sample

@sample_route.get("/get_name/{sample_name}", response_model=list[Sample])
async def get_sample_sku(sample_sku: str, session: SessionDep):
    sample = await sample_service.get_sample_sku(sample_sku, session)
    if sample is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    return sample

@sample_route.post("/", response_model=Sample)
async def create_sample(sample_data: CreateSampleScheme, session: SessionDep) -> dict:
    new_sample = await sample_service.create_sample(sample_data, session)
    return new_sample

@sample_route.put("/{sample_item}", response_model=Sample)
async def update_sample(sample_item: str, data_update: CreateSampleScheme, session: SessionDep):
    updated_sample = await sample_service.update_sample(sample_item, data_update, session)
    if updated_sample is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    else:
        return updated_sample

@sample_route.delete("/{sample_item}", response_model=Sample)
async def delete_sample(sample_item: str, session: SessionDep):
    sample_to_deleted = await sample_service.delete_sample(sample_item, session)
    if sample_to_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    else:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Sample is deleted")
