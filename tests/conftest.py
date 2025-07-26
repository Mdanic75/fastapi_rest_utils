import pytest
from unittest.mock import Mock, AsyncMock
from typing import List, Dict, Any
from pydantic import BaseModel
from fastapi import Request


class TestProductSchema(BaseModel):
    id: int
    name: str
    price: float


class TestProductCreateSchema(BaseModel):
    name: str
    price: float


class TestProductUpdateSchema(BaseModel):
    name: str = None
    price: float = None




@pytest.fixture
def mock_viewset_data():
    """Mock data for viewset tests"""
    return [
        {"id": 1, "name": "Product 1", "price": 10.0},
        {"id": 2, "name": "Product 2", "price": 20.0}
    ]


@pytest.fixture
def mock_dependency():
    """Mock dependency for testing"""
    return Mock()


@pytest.fixture
def mock_async_dependency():
    """Mock async dependency for testing"""
    return AsyncMock()


class MockViewSetWithRoutes:
    """Minimal mock with only routes_config method"""
    dependency: List[Any] = []
    
    def routes_config(self):
        return [
            {
                "path": "",
                "method": "GET",
                "endpoint_name": "test",
                "response_model": TestProductSchema
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
                }
            }
        ]

    def test(self, *args, **kwargs):
        pass

    def create(self, *args, **kwargs):
        pass

@pytest.fixture
def mock_viewset_with_routes():
    """Mock viewset with routes_config only"""
    return MockViewSetWithRoutes