"""Protocols for fastapi-rest-utils viewsets and router interfaces."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, TypedDict


class RouteConfigDictBase(TypedDict):
    """Base configuration for API routes."""

    path: str
    method: str
    endpoint_name: str
    response_model: Any


class RouteConfigDict(RouteConfigDictBase, total=False):
    """Extended route configuration with optional fields."""

    dependencies: list
    tags: list[str]
    openapi_extra: dict
    name: str
    summary: str
    description: str
    deprecated: bool
    include_in_schema: bool
    kwargs: dict  # For passing custom arguments


class ViewProtocol(ABC):
    """Protocol for a view that must provide a schema_config property and a routes_config method.

    The routes_config method returns a RouteConfigDict representing keyword arguments to be passed to the router.
    The schema_config property stores configuration such as response schemas, e.g. {"list": {"response": MySchema}}.
    """

    @property
    @abstractmethod
    def schema_config(self) -> dict[str, Any]:
        """Mandatory attribute that must return the schema configuration for the view."""
        ...

    @abstractmethod
    def routes_config(self) -> list[RouteConfigDict]:
        """Return the routes configuration for the view."""
        ...


class RouterProtocol(ABC):
    """Protocol for an extended APIRouter that must implement register_view and register_viewset methods."""

    @abstractmethod
    def register_viewset(
        self,
        viewset_class: type[ViewProtocol],
        prefix: str,
        tags: list[str | Enum] | None = None,
        **kwargs: dict,
    ) -> None:
        """Register the viewset's routes with this router."""
        ...
