from fastapi import FastAPI
from app.sample.routes import sample_route
from app.delivery_plan.routes import delivery_plan_route
from app.delivery.routes import delivery_route
#from app.info_sample.routes import info_sample_route
from app.status_report.routes import status_report_route
from app.config import Config



description = """
A REST API for a Raw Material Sample web service.

This REST API is able to:
- Create CRUD sample,...
"""

version_prefix = Config.VERSION

app = FastAPI(
    title="Sample Management",
    description=description,
    version=version_prefix,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Hao Nguyen",
        "url": "https://github.com/haontuhcmut",
        "email": "nguyenminhhao1188@gmail.com",
    },
    openapi_url=f"/{version_prefix}/openapi.json",
    docs_url=f"/{version_prefix}/docs",
    redoc_url=f"/{version_prefix}/redoc",
)


app.include_router(sample_route, prefix=f"/{version_prefix}/sample", tags=["sample"])
app.include_router(delivery_plan_route, prefix=f"/{version_prefix}/delivery_plan", tags=["delivery plan"])
app.include_router(delivery_route, prefix=f"/{version_prefix}/delivery", tags=["delivery"])
app.include_router(status_report_route, prefix=f"/{version_prefix}/status", tags=["status"])
#app.include_router(info_sample_route, prefix=f"/{version_prefix}/info_sample", tags=["info sample"])
