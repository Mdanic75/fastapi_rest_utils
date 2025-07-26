from typing import Any, Dict, List, Type
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import Request
from pydantic import BaseModel


class TestProductSchema(BaseModel):
    id: int
    name: str
    price: float


class TestProductCreateSchema(BaseModel):
    name: str
    price: float


class TestProductUpdateSchema(BaseModel):
    name: str | None = None
    price: float | None = None


@pytest.fixture
def mock_viewset_data() -> List[Dict[str, Any]]:
    """Mock data for viewset tests"""
    return [
        {"id": 1, "name": "Product 1", "price": 10.0},
        {"id": 2, "name": "Product 2", "price": 20.0},
    ]


@pytest.fixture
def mock_dependency() -> Mock:
    """Mock dependency for testing"""
    return Mock()


@pytest.fixture
def mock_async_dependency() -> AsyncMock:
    """Mock async dependency for testing"""
    return AsyncMock()


class MockViewSetWithRoutes:
    """Minimal mock with only routes_config method"""

    dependency: List[Any] = []

    def routes_config(self) -> List[Dict[str, Any]]:
        return [
            {
                "path": "",
                "method": "GET",
                "endpoint_name": "test",
                "response_model": TestProductSchema,
            },
            {
                "path": "/",
                "method": "POST",
                "endpoint_name": "create",
                "response_model": TestProductSchema,
                "payload_model": TestProductCreateSchema,
                "openapi_extra": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": TestProductCreateSchema.model_json_schema()
                            }
                        }
                    }
                },
            },
        ]

    def test(self, *args: Any, **kwargs: Any) -> None:
        pass

    def create(self, *args: Any, **kwargs: Any) -> None:
        pass


@pytest.fixture
def mock_viewset_with_routes() -> Type[MockViewSetWithRoutes]:
    """Mock viewset with routes_config only"""
    return MockViewSetWithRoutes
