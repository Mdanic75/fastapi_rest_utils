from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import HTTPException, Request

from fastapi_rest_utils.viewsets.sqlalchemy import (
    SQLAlchemyCreateView,
    SQLAlchemyDeleteView,
    SQLAlchemyListView,
    SQLAlchemyRetrieveView,
    SQLAlchemyUpdateView,
)


# Minimal mock SQLAlchemy model
class MockProduct:
    def __init__(
        self, id: int = 1, name: str = "Test Product", price: float = 10.0
    ) -> None:
        self.id = id
        self.name = name
        self.price = price


# Minimal mock SQLAlchemy result
class MockResult:
    def __init__(self, data: Any) -> None:
        self._data = data

    def scalars(self) -> Any:
        return self

    def all(self) -> Any:
        return self._data

    def scalar_one_or_none(self) -> Any:
        return self._data


class MockSession:
    def __init__(self, data: Any = None) -> None:
        self.data = data
        self.committed = False
        self.added: list[Any] = []
        self.refreshed: list[Any] = []
        self.deleted = False

    async def execute(self, stmt: Any) -> MockResult:
        return MockResult(self.data)

    async def commit(self) -> None:
        self.committed = True

    async def refresh(self, obj: Any) -> None:
        self.refreshed.append(obj)

    def add(self, obj: Any) -> None:
        self.added.append(obj)


@pytest.fixture
def mock_request() -> Request:
    req = Mock(spec=Request)
    req.state.db = MockSession()
    return req
