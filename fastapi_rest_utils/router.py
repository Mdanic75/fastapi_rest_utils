"""Router utilities for fastapi-rest-utils, including RestRouter and router_from_viewset."""

from enum import Enum
from typing import Any, List, Optional, Type

from fastapi import APIRouter

from fastapi_rest_utils.protocols import ViewProtocol


class RestRouter(APIRouter):
    """
    An extended APIRouter which includes methods to register viewsets and individual views.

    The viewset should implement BaseViewSetProtocol.
    """

    def register_viewset(
        self,
        viewset_class: Type[ViewProtocol],
        prefix: str,
        tags: Optional[List[str | Enum]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Register the viewset's routes with this router.

        Args:
            viewset_class (Type[ViewProtocol]): The viewset class containing route configurations.
            prefix (str): The URL prefix for the viewset.
            tags (Optional[List[str | Enum]]): Tags for API documentation purposes.
            **kwargs: Additional keyword arguments passed to add_api_route.
        """
        viewset = viewset_class()
        routes_config = viewset.routes_config()

        for route_config in routes_config:
            endpoint = getattr(viewset, route_config["endpoint_name"])
            path = f"{prefix}{route_config['path']}"
            response_model = route_config.get("response_model")

            openapi_extra = route_config.get("openapi_extra")
            route_dependencies = route_config.get("dependencies", [])
            kwargs_dependencies = kwargs.pop("dependencies", [])
            all_dependencies = route_dependencies + kwargs_dependencies

            self.add_api_route(
                path=path,
                endpoint=endpoint,
                methods=[route_config["method"]],
                tags=tags,
                response_model=response_model,
                openapi_extra=openapi_extra,
                dependencies=all_dependencies,
                **kwargs,
            )
