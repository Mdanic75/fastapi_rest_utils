"""Main package for fastapi-rest-utils."""

__version__ = "0.1.0"

from fastapi_rest_utils.deps import auth_dep_injector, db_dep_injector
from fastapi_rest_utils.router import RestRouter
from fastapi_rest_utils.viewsets.base import BaseView
from fastapi_rest_utils.viewsets.sqlalchemy import ModelViewSet

__all__ = [
    "__version__",
    "BaseView",
    "ModelViewSet",
    "RestRouter",
    "db_dep_injector",
    "auth_dep_injector",
]
