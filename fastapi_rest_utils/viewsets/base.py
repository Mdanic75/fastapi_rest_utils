"""Base viewsets for fastapi-rest-utils."""
from fastapi_rest_utils.protocols import ViewProtocol, RouteConfigDict, BaseViewSetProtocol
from typing import Dict, Any, List, Callable
from fastapi import Request
from pydantic import BaseModel


class ListView(ViewProtocol):
    """
    Subclasses must set schema_config to include a response schema, e.g. {"list": {"response": MySchema}}.
    """
    schema_config: Dict[str, Any]

    @classmethod
    def route_config(cls) -> RouteConfigDict:
        response_model = cls.schema_config.get("list", {}).get("response")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise NotImplementedError("schema_config['list']['response'] must be set to a Pydantic BaseModel subclass.")
        return {
            'path': '',
            'method': 'GET',
            'endpoint_name': 'list',
            'response_model': response_model
        }

    async def list(self, request: Request, *args, **kwargs) -> Any:
        objects = await self.get_objects(request, *args, **kwargs)
        return objects

    async def get_objects(self, request: Request, *args, **kwargs) -> Any:
        """
        Should return a list or iterable of objects that can be parsed by the Pydantic response_model.
        For example, a list of dicts or ORM models compatible with the response_model.
        """
        raise NotImplementedError("Subclasses must implement get_objects()")

class RetrieveView(ViewProtocol):
    schema_config: Dict[str, Any]

    @classmethod
    def route_config(cls) -> RouteConfigDict:
        response_model = cls.schema_config.get("retrieve", {}).get("response")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise NotImplementedError("schema_config['retrieve']['response'] must be set to a Pydantic BaseModel subclass.")
        return {
            'path': '/{id}',
            'method': 'GET',
            'endpoint_name': 'retrieve',
            'response_model': response_model
        }

    async def retrieve(self, request: Request, id: Any, *args, **kwargs) -> Any:
        obj = await self.get_object(request, id, *args, **kwargs)
        return obj

    async def get_object(self, request: Request, id: Any, *args, **kwargs) -> Any:
        """
        Should return a single object (dict or ORM model) that can be parsed by the response_model.
        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement get_object()")

class CreateView(ViewProtocol):
    schema_config: Dict[str, Any]

    @classmethod
    def route_config(cls) -> RouteConfigDict:
        response_model = cls.schema_config.get("create", {}).get("response")
        payload_model = cls.schema_config.get("create", {}).get("payload")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise NotImplementedError("schema_config['create']['response'] must be set to a Pydantic BaseModel subclass.")
        if payload_model is None or not issubclass(payload_model, BaseModel):
            raise NotImplementedError("schema_config['create']['payload'] must be set to a Pydantic BaseModel subclass.")
        return {
            'path': '',
            'method': 'POST',
            'endpoint_name': 'create',
            'response_model': response_model,
            'openapi_extra': {'requestBody': {'content': {'application/json': {'schema': payload_model.model_json_schema()}}, 'required': True}}
        }

    async def create(self, request: Request, payload: Any, *args, **kwargs) -> Any:
        obj = await self.create_object(request, payload, *args, **kwargs)
        return obj

    async def create_object(self, request: Request, payload: Any, *args, **kwargs) -> Any:
        """
        Should create and return a new object that can be parsed by the response_model.
        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement create_object()")

class UpdateView(ViewProtocol):
    schema_config: Dict[str, Any]

    @classmethod
    def route_config(cls) -> RouteConfigDict:
        response_model = cls.schema_config.get("update", {}).get("response")
        payload_model = cls.schema_config.get("update", {}).get("payload")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise NotImplementedError("schema_config['update']['response'] must be set to a Pydantic BaseModel subclass.")
        if payload_model is None or not issubclass(payload_model, BaseModel):
            raise NotImplementedError("schema_config['update']['payload'] must be set to a Pydantic BaseModel subclass.")
        return {
            'path': '/{id}',
            'method': 'PUT',
            'endpoint_name': 'update',
            'response_model': response_model,
            'openapi_extra': {'requestBody': {'content': {'application/json': {'schema': payload_model.model_json_schema()}}, 'required': True}}
        }

    async def update(self, request: Request, id: Any, payload: Any, *args, **kwargs) -> Any:
        obj = await self.update_object(request, id, payload, *args, **kwargs)
        return obj

    async def update_object(self, request: Request, id: Any, payload: Any, *args, **kwargs) -> Any:
        """
        Should update and return an object that can be parsed by the response_model.
        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement update_object()")

class PartialUpdateView(ViewProtocol):
    schema_config: Dict[str, Any]

    @classmethod
    def route_config(cls) -> RouteConfigDict:
        response_model = cls.schema_config.get("partial_update", {}).get("response")
        payload_model = cls.schema_config.get("partial_update", {}).get("payload")
        if response_model is None or not issubclass(response_model, BaseModel):
            raise NotImplementedError("schema_config['partial_update']['response'] must be set to a Pydantic BaseModel subclass.")
        if payload_model is None or not issubclass(payload_model, BaseModel):
            raise NotImplementedError("schema_config['partial_update']['payload'] must be set to a Pydantic BaseModel subclass.")
        return {
            'path': '/{id}',
            'method': 'PATCH',
            'endpoint_name': 'partial_update',
            'response_model': response_model,
            'openapi_extra': {'requestBody': {'content': {'application/json': {'schema': payload_model.model_json_schema()}}, 'required': True}}
        }

    async def partial_update(self, request: Request, id: Any, payload: Any, *args, **kwargs) -> Any:
        obj = await self.update_partial_object(request, id, payload, *args, **kwargs)
        return obj

    async def update_partial_object(self, request: Request, id: Any, payload: Any, *args, **kwargs) -> Any:
        """
        Should partially update and return an object that can be parsed by the response_model.
        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement update_partial_object()")

class DeleteView(ViewProtocol):
    schema_config: Dict[str, Any]

    @classmethod
    def route_config(cls) -> RouteConfigDict:
        # For delete, we do not require a response_model; just return status
        return {
            'path': '/{id}',
            'method': 'DELETE',
            'endpoint_name': 'delete',
            'response_model': None
        }

    async def delete(self, request: Request, id: Any, *args, **kwargs) -> Any:
        result = await self.delete_object(request, id, *args, **kwargs)
        return result

    async def delete_object(self, request: Request, id: Any, *args, **kwargs) -> Any:
        """
        Should delete the object and return a response (e.g., status or deleted object).
        ORM-related logic must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement delete_object()")

class BaseViewSet(BaseViewSetProtocol):
    """
    Base implementation of a viewset that aggregates route configs from all immediate parent view classes.
    Inherit from this class and from any number of view classes (e.g., ListView, RetrieveView, etc.).
    The routes_config classmethod will collect all route configs from immediate parent view classes that implement route_config.
    """
    dependency: List[Callable[..., Any]]

    def routes_config(self) -> List[RouteConfigDict]:
        routes: List[RouteConfigDict] = []
        for base in self.__class__.__bases__:
            route_config = getattr(base, "route_config", None)
            if callable(route_config):
                config = route_config()
                if config:
                    routes.append(config)
        return routes 