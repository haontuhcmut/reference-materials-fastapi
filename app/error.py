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
