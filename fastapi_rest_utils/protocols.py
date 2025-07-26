"""Protocols for fastapi-rest-utils viewsets and router interfaces."""
from typing import Protocol, Any, List, TypedDict, Callable, Optional, Dict

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

class ViewProtocol(Protocol):
    """
    Protocol for a view that must provide a schema_config attribute and a classmethod route_config.
    The route_config classmethod returns a RouteConfigDict representing keyword arguments to be passed to the router.
    The schema_config attribute stores configuration such as response schemas, e.g. {"list": {"response": MySchema}}.
    """
    schema_config: Dict[str, Any]
    
    @classmethod
    def route_config(cls) -> RouteConfigDict: ...

class BaseViewSetProtocol(Protocol):
    """
    Protocol for a base viewset, requiring only a classmethod routes_config and a dependency attribute.
    Intended to be extended with view classes implementing the routes_config classmethod.
    This makes it agnostic to model and implementation details.
    The routes_config classmethod returns a list of RouteConfigDicts, each representing a route from the viewset.
    The dependency attribute should provide a list of callables for database session or other required dependencies.
    """
    dependency: List[Callable[..., Any]]
    def routes_config(self) -> List[RouteConfigDict]: ...

class RouterProtocol(Protocol):
    """
    Protocol for an extended APIRouter that must implement register_view and register_viewset methods.
    """
    def register_view(self, view: ViewProtocol, *args, **kwargs) -> None: ...
    def register_viewset(self, viewset: BaseViewSetProtocol, *args, **kwargs) -> None: ... 
