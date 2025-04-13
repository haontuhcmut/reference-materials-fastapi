from typing import Any, Callable
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import FastAPI, status


class ExceptionRegister(Exception):
    """This is the base class for all exceptions"""

    pass


class CategoryNotFound(ExceptionRegister):
    """Category not found"""

    pass

class PTSChemeNotFound(ExceptionRegister):
    """PT scheme not found"""

    pass

class ProductNotFound(ExceptionRegister):
    """Product not found"""

    pass

class BomNotFound(ExceptionRegister):
    """Bill of material not found"""

    pass

class MaterialNotFound(ExceptionRegister):
    """Material not found"""

    pass

class ItemTypeNotFound(ExceptionRegister):
    """Item type not found"""

    pass


class WarehouseNotFound(ExceptionRegister):
    """Warehouse not found"""

    pass

class TransactionNotFound(ExceptionRegister):
    """Transaction not found"""

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
        PTSChemeNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "PT scheme not found",
                "error_code": "pt_scheme_not_found"
            },
        ),
    )

    app.add_exception_handler(
        ProductNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Product not found",
                "error_code": "product_not_found"
            },
        ),
    )

    app.add_exception_handler(
        BomNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Bill of material not found",
                "error_code": "bom_not_found"
            },
        ),
    )

    app.add_exception_handler(
        MaterialNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Material not found",
                "error_code": "material_not_found"
            },
        ),
    )

    app.add_exception_handler(
        ItemTypeNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Item type not found",
                "error_code": "item_type_not_found"
            },
        ),
    )


    app.add_exception_handler(
        WarehouseNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Warehouse not found",
                "error_code": "warehouse_not_found"
            },
        ),
    )


    app.add_exception_handler(
        TransactionNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Transaction not found",
                "error_code": "transaction_not_found"
            },
        ),
    )