from fastapi import FastAPI
from app.error import register_all_errors
from app.config import Config

from app.category.route import category_route
from app.pt_scheme.route import pt_scheme_route



description = """
A REST API for a Laboratory Information Management Systems web service.

This REST API is able to:
- Create CRUD,...
"""

version_prefix = Config.VERSION

app = FastAPI(
    title="Laboratory Information Management Systems",
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

register_all_errors(app)

app.include_router(category_route, prefix=f"/{version_prefix}/category", tags=["category"])
app.include_router(pt_scheme_route, prefix=f"/{version_prefix}/pt_scheme", tags=["pt_scheme"])
