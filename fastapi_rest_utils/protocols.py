"""Protocols for fastapi-rest-utils viewsets and router interfaces."""
from typing import Any, List, Type, TypedDict, Dict
from abc import ABC, abstractmethod

class RouteConfigDictBase(TypedDict):
    path: str
    method: str
    endpoint_name: str
    response_model: Any

class RouteConfigDict(RouteConfigDictBase, total=False):
    dependencies: List[Any]
    tags: List[str]
    openapi_extra: dict
    name: str
    summary: str
    description: str
    deprecated: bool
    include_in_schema: bool
    kwargs: dict  # For passing custom arguments

class ViewProtocol(ABC):
    """
    Protocol for a view that must provide a schema_config attribute and a classmethod route_config.
    The route_config classmethod returns a RouteConfigDict representing keyword arguments to be passed to the router.
    The schema_config attribute stores configuration such as response schemas, e.g. {"list": {"response": MySchema}}.
    """
    schema_config: Dict[str, Any]
    
    @abstractmethod
    def routes_config(self) -> List[RouteConfigDict]: ...


class RouterProtocol(ABC):
    """
    Protocol for an extended APIRouter that must implement register_view and register_viewset methods.
    """
    # @abstractmethod
    # def register_view(self, view: ViewProtocol, *args, **kwargs) -> None: ...
    @abstractmethod
    def register_viewset(self, viewset: Type[ViewProtocol], *args, **kwargs) -> None: ... 
