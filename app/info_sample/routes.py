from fastapi import APIRouter
from app.db.dependencies import SessionDep
from app.info_sample.services import InfoSampleServices
from app.info_sample.schemas import SampleRead

info_sample_services = InfoSampleServices()
info_sample_route = APIRouter()

@info_sample_route.get("/info_sample", response_model= list[SampleRead])
async def get_info_sample(session:SessionDep):
    sample = await info_sample_services.get_info_samples(session)
    return sample
