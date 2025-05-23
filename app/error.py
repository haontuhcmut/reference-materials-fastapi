from typing import Any, Callable
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import FastAPI, status


class ExceptionRegister(Exception):
    """This is the base class for all exceptions"""

    pass


class InvalidIDFormat(ExceptionRegister):
    """Invalid ID format"""

    pass


class CategoryNotFound(ExceptionRegister):
    """Category not found"""

    pass


class CategoryAlreadyExist(ExceptionRegister):
    """Category already exist"""

    pass


class PTSChemeNotFound(ExceptionRegister):
    """PT scheme not found"""

    pass


class PTSchemeAlreadyExist(ExceptionRegister):
    """PT scheme already exist"""


class ProductNotFound(ExceptionRegister):
    """Product not found"""

    pass


class ProductAlreadyExist(ExceptionRegister):
    """Product already exist"""


class BomNotFound(ExceptionRegister):
    """Bill of material not found"""

    pass


class MaterialNotFound(ExceptionRegister):
    """Material not found"""

    pass


class WarehouseNotFound(ExceptionRegister):
    """Warehouse not found"""

    pass


def create_exception_handler(
    status_code: int, detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(requests: Request, exc: ExceptionRegister):
        return JSONResponse(content=detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        CategoryNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Category not found",
                "error_code": "category_not_found",
            },
        ),
    )

    app.add_exception_handler(
        InvalidIDFormat,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Invalid ID format", "error_code": "invalid_id_format"},
        ),
    )

    app.add_exception_handler(
        CategoryAlreadyExist,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Category name already exist",
                "error_code": "category_name_already_exist",
            },
        ),
    )

    app.add_exception_handler(
        PTSChemeNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "PT scheme not found",
                "error_code": "pt_scheme_not_found",
            },
        ),
    )

    app.add_exception_handler(
        PTSchemeAlreadyExist,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "PT scheme code already exist",
                "error_code": "pt_scheme_code_already_exist",
            },
        ),
    )

    app.add_exception_handler(
        ProductNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Product not found", "error_code": "product_not_found"},
        ),
    )

    app.add_exception_handler(
        ProductAlreadyExist,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Product already exist",
                "error_code": "product_already_exist",
            },
        ),
    )

    app.add_exception_handler(
        BomNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Bill of material not found",
                "error_code": "bom_not_found",
            },
        ),
    )

    app.add_exception_handler(
        MaterialNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Material not found",
                "error_code": "material_not_found",
            },
        ),
    )

    app.add_exception_handler(
        WarehouseNotFound,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Warehouse not found",
                "error_code": "warehouse_not_found",
            },
        ),
    )
