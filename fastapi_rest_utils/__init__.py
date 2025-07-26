"""
FastAPI REST Utils - Utilities for building REST APIs with FastAPI
"""

__version__ = "0.1.0"

from .deps import get_db
from .router import router_from_viewset
from .viewsets.base import BaseViewSet as ViewSet
from .viewsets.base import BaseViewSet
from .viewsets.sqlalchemy import SQLAlchemyViewSet

__all__ = [
    "__version__",
    "ViewSet",
    "BaseViewSet", 
    "SQLAlchemyViewSet",
    "router_from_viewset",
    "get_db",
]
