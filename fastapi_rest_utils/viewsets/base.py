"""Base viewsets for fastapi-rest-utils."""

from typing import Any

from fastapi import Body, Request
from pydantic import BaseModel

from fastapi_rest_utils.errors import MissingSchemaConfigError
from fastapi_rest_utils.protocols import RouteConfigDict, ViewProtocol


class BaseView(ViewProtocol):
    """Base view class that provides a default routes_config method."""

    def routes_config(self) -> list[RouteConfigDict]:
        """Return empty routes configuration.

        Subclasses must implement routes_config.
        """
        return []


class ListView(BaseView):
    """Subclasses must set schema_config to include a response schema, e.g. {"list": {"response": MySchema}}."""

    def routes_config(self) -> list[RouteConfigDict]:  # noqa: D102
        routes = super().routes_config()
        response_model = self.schema_config.get("list", {}).get("response")
        if response_model is None:
            raise MissingSchemaConfigError(self.__class__.__name__, "list", "response")
        routes.append(
            {
                "path": "",
                "method": "GET",
                "endpoint_name": "list",
                "response_model": response_model,
            },
        )
        return routes

    async def list(self, request: Request) -> Any:  # noqa: ANN401
        """List all objects."""
        return await self.get_objects(request)

    async def get_objects(self, request: Request) -> Any:  # noqa: ANN401
        """Return a list or iterable of objects that can be parsed by the Pydantic response_model.

        For example, a list of dicts or ORM models compatible with the response_model.
        """
        raise NotImplementedError


class RetrieveView(BaseView):
    """View for retrieving a single object by ID."""

    def routes_config(self) -> list[RouteConfigDict]:  # noqa: D102
        routes = super().routes_config()
        response_model = self.schema_config.get("retrieve", {}).get("response")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise MissingSchemaConfigError(self.__class__.__name__, "retrieve", "response")
        routes.append(
            {
                "path": "/{id}",
                "method": "GET",
                "endpoint_name": "retrieve",
                "response_model": response_model,
            },
        )
        return routes

    async def retrieve(self, request: Request, pk: Any) -> Any:  # noqa: ANN401
        """Retrieve a single object by ID."""
        return await self.get_object(request, pk)

    async def get_object(self, request: Request, pk: Any) -> Any:  # noqa: ANN401
        """Return a single object (dict or ORM model) that can be parsed by the response_model.

        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError


class CreateView(BaseView):
    """View for creating new objects."""

    def routes_config(self) -> list[RouteConfigDict]:  # noqa: D102
        routes = super().routes_config()
        response_model = self.schema_config.get("create", {}).get("response")
        payload_model = self.schema_config.get("create", {}).get("payload")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise MissingSchemaConfigError(self.__class__.__name__, "create", "response")
        if payload_model is None or not issubclass(payload_model, BaseModel):
            raise MissingSchemaConfigError(self.__class__.__name__, "create", "payload")
        routes.append(
            {
                "path": "",
                "method": "POST",
                "endpoint_name": "create",
                "response_model": response_model,
                "openapi_extra": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": payload_model.model_json_schema(),
                            },
                        },
                        "required": True,
                    },
                },
            },
        )
        return routes

    async def create(self, request: Request, payload: dict = Body(...)) -> Any:  # noqa: ANN401
        """Create a new object."""
        return await self.create_object(request, payload)

    async def create_object(self, request: Request, payload: Any) -> Any:  # noqa: ANN401
        """Create and return a new object that can be parsed by the response_model.

        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError


class UpdateView(BaseView):
    """View for updating objects by ID."""

    def routes_config(self) -> list[RouteConfigDict]:  # noqa: D102
        routes = super().routes_config()
        response_model = self.schema_config.get("update", {}).get("response")
        payload_model = self.schema_config.get("update", {}).get("payload")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise MissingSchemaConfigError(self.__class__.__name__, "update", "response")
        if payload_model is None or not issubclass(payload_model, BaseModel):
            raise MissingSchemaConfigError(self.__class__.__name__, "update", "payload")
        routes.append(
            {
                "path": "/{id}",
                "method": "PUT",
                "endpoint_name": "update",
                "response_model": response_model,
                "openapi_extra": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": payload_model.model_json_schema(),
                            },
                        },
                        "required": True,
                    },
                },
            },
        )
        return routes

    async def update(self, request: Request, pk: Any, payload: dict = Body(...)) -> Any:  # noqa: ANN401
        """Update an object by ID."""
        return await self.update_object(request, pk, payload)

    async def update_object(self, request: Request, pk: Any, payload: Any) -> Any:  # noqa: ANN401
        """Update and return an object that can be parsed by the response_model.

        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError


class PartialUpdateView(BaseView):
    """View for partially updating objects by ID."""

    def routes_config(self) -> list[RouteConfigDict]:  # noqa: D102
        routes = super().routes_config()
        response_model = self.schema_config.get("partial_update", {}).get("response")
        payload_model = self.schema_config.get("partial_update", {}).get("payload")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise MissingSchemaConfigError(self.__class__.__name__, "partial_update", "response")
        if payload_model is None or not issubclass(payload_model, BaseModel):
            raise MissingSchemaConfigError(self.__class__.__name__, "partial_update", "payload")
        routes.append(
            {
                "path": "/{id}",
                "method": "PATCH",
                "endpoint_name": "partial_update",
                "response_model": response_model,
                "openapi_extra": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": payload_model.model_json_schema(),
                            },
                        },
                        "required": True,
                    },
                },
            },
        )
        return routes

    async def partial_update(self, request: Request, pk: Any, payload: dict = Body(...)) -> Any:  # noqa: ANN401
        """Update an object by ID."""
        return await self.update_partial_object(request, pk, payload)

    async def update_partial_object(self, request: Request, pk: Any, payload: Any) -> Any:  # noqa: ANN401
        """Update and return an object that can be parsed by the response_model.

        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError


class DeleteView(BaseView):
    """View for deleting objects by ID."""

    def routes_config(self) -> list[RouteConfigDict]:  # noqa: D102
        routes = super().routes_config()
        # For delete, we do not require a response_model; just return status
        routes.append(
            {
                "path": "/{id}",
                "method": "DELETE",
                "endpoint_name": "delete",
                "response_model": None,
            },
        )
        return routes

    async def delete(self, request: Request, pk: Any) -> Any:  # noqa: ANN401
        """Delete an object by ID."""
        return await self.delete_object(request, pk)

    async def delete_object(self, request: Request, pk: Any) -> Any:  # noqa: ANN401
        """Delete the object and return a response (e.g., status or deleted object).

        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError
