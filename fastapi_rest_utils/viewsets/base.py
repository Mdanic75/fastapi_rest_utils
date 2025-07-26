"""Base viewsets for fastapi-rest-utils."""

from abc import abstractmethod
from typing import Any, Dict, List

from fastapi import Body, Request
from pydantic import BaseModel

from fastapi_rest_utils.protocols import RouteConfigDict, ViewProtocol


class BaseView(ViewProtocol):
    """
    Base view class that provides a default routes_config method.
    """

    @property
    @abstractmethod
    def schema_config(self) -> Dict[str, Any]: ...

    def routes_config(self) -> List[RouteConfigDict]:
        return []


class ListView(BaseView):
    """
    Subclasses must set schema_config to include a response schema, e.g. {"list": {"response": MySchema}}.
    """

    def routes_config(self) -> List[RouteConfigDict]:
        routes = super().routes_config()
        response_model = self.schema_config.get("list", {}).get("response")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise NotImplementedError(
                "schema_config['list']['response'] must be set to a Pydantic BaseModel subclass."
            )
        routes.append(
            {
                "path": "",
                "method": "GET",
                "endpoint_name": "list",
                "response_model": response_model,
            }
        )
        return routes

    async def list(self, request: Request) -> Any:
        objects = await self.get_objects(request)
        return objects

    async def get_objects(self, request: Request) -> Any:
        """
        Should return a list or iterable of objects that can be parsed by the Pydantic response_model.
        For example, a list of dicts or ORM models compatible with the response_model.
        """
        raise NotImplementedError("Subclasses must implement get_objects()")


class RetrieveView(BaseView):

    def routes_config(self) -> List[RouteConfigDict]:
        routes = super().routes_config()
        response_model = self.schema_config.get("retrieve", {}).get("response")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise NotImplementedError(
                "schema_config['retrieve']['response'] must be set to a Pydantic BaseModel subclass."
            )
        routes.append(
            {
                "path": "/{id}",
                "method": "GET",
                "endpoint_name": "retrieve",
                "response_model": response_model,
            }
        )
        return routes

    async def retrieve(self, request: Request, id: Any) -> Any:
        obj = await self.get_object(request, id)
        return obj

    async def get_object(self, request: Request, id: Any) -> Any:
        """
        Should return a single object (dict or ORM model) that can be parsed by the response_model.
        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement get_object()")


class CreateView(BaseView):

    def routes_config(self) -> List[RouteConfigDict]:
        routes = super().routes_config()
        response_model = self.schema_config.get("create", {}).get("response")
        payload_model = self.schema_config.get("create", {}).get("payload")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise NotImplementedError(
                "schema_config['create']['response'] must be set to a Pydantic BaseModel subclass."
            )
        if payload_model is None or not issubclass(payload_model, BaseModel):
            raise NotImplementedError(
                "schema_config['create']['payload'] must be set to a Pydantic BaseModel subclass."
            )
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
                                "schema": payload_model.model_json_schema()
                            }
                        },
                        "required": True,
                    }
                },
            }
        )
        return routes

    async def create(self, request: Request, payload: dict = Body(...)) -> Any:
        obj = await self.create_object(request, payload)
        return obj

    async def create_object(self, request: Request, payload: Any) -> Any:
        """
        Should create and return a new object that can be parsed by the response_model.
        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement create_object()")


class UpdateView(BaseView):

    def routes_config(self) -> List[RouteConfigDict]:
        routes = super().routes_config()
        response_model = self.schema_config.get("update", {}).get("response")
        payload_model = self.schema_config.get("update", {}).get("payload")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise NotImplementedError(
                "schema_config['update']['response'] must be set to a Pydantic BaseModel subclass."
            )
        if payload_model is None or not issubclass(payload_model, BaseModel):
            raise NotImplementedError(
                "schema_config['update']['payload'] must be set to a Pydantic BaseModel subclass."
            )
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
                                "schema": payload_model.model_json_schema()
                            }
                        },
                        "required": True,
                    }
                },
            }
        )
        return routes

    async def update(self, request: Request, id: Any, payload: dict) -> Any:
        obj = await self.update_object(request, id, payload)
        return obj

    async def update_object(self, request: Request, id: Any, payload: Any) -> Any:
        """
        Should update and return an object that can be parsed by the response_model.
        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement update_object()")


class PartialUpdateView(BaseView):

    def routes_config(self) -> List[RouteConfigDict]:
        routes = super().routes_config()
        response_model = self.schema_config.get("partial_update", {}).get("response")
        payload_model = self.schema_config.get("partial_update", {}).get("payload")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise NotImplementedError(
                "schema_config['partial_update']['response'] must be set to a Pydantic BaseModel subclass."
            )
        if payload_model is None or not issubclass(payload_model, BaseModel):
            raise NotImplementedError(
                "schema_config['partial_update']['payload'] must be set to a Pydantic BaseModel subclass."
            )
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
                                "schema": payload_model.model_json_schema()
                            }
                        },
                        "required": True,
                    }
                },
            }
        )
        return routes

    async def partial_update(self, request: Request, id: Any, payload: dict) -> Any:
        obj = await self.update_partial_object(request, id, payload)
        return obj

    async def update_partial_object(
        self, request: Request, id: Any, payload: Any
    ) -> Any:
        """
        Should partially update and return an object that can be parsed by the response_model.
        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement update_partial_object()")


class DeleteView(BaseView):

    def routes_config(self) -> List[RouteConfigDict]:
        routes = super().routes_config()
        # For delete, we do not require a response_model; just return status
        routes.append(
            {
                "path": "/{id}",
                "method": "DELETE",
                "endpoint_name": "delete",
                "response_model": None,
            }
        )
        return routes

    async def delete(self, request: Request, id: Any) -> Any:
        result = await self.delete_object(request, id)
        return result

    async def delete_object(self, request: Request, id: Any) -> Any:
        """
        Should delete the object and return a response (e.g., status or deleted object).
        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement delete_object()")
