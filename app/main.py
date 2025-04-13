from fastapi import FastAPI
from app.error import register_all_errors
from app.config import Config

from app.category.route import category_route
from app.pt_scheme.route import pt_scheme_route
from app.product.route import product_route
from app.bom.route import bom_route
from app.material.route import material_route
from app.item_type.route import item_type_route
from app.warehouse.route import warehouse_route
from app.transaction.route import transaction_route


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
app.include_router(product_route, prefix=f"/{version_prefix}/product", tags=["product"])
app.include_router(bom_route, prefix=f"/{version_prefix}/bom", tags=["bom"])
app.include_router(material_route, prefix=f"/{version_prefix}/material", tags=["material"])
app.include_router(item_type_route, prefix=f"/{version_prefix}/item_type", tags=["item_type"])
app.include_router(warehouse_route, prefix=f"/{version_prefix}/warehouse", tags=["warehouse"])
app.include_router(transaction_route, prefix=f"/{version_prefix}/transaction", tags=["transaction"])






