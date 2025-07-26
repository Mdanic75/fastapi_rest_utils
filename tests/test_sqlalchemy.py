import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import HTTPException, Request
from fastapi_rest_utils.viewsets.sqlalchemy import (
    SQLAlchemyListView, SQLAlchemyRetrieveView, SQLAlchemyCreateView,
    SQLAlchemyUpdateView, SQLAlchemyDeleteView
)

# Minimal mock SQLAlchemy model
class MockProduct:
    def __init__(self, id=1, name="Test Product", price=10.0):
        self.id = id
        self.name = name
        self.price = price

# Minimal mock SQLAlchemy result
class MockResult:
    def __init__(self, data):
        self._data = data
    def scalars(self):
        return self
    def all(self):
        return self._data
    def scalar_one_or_none(self):
        return self._data

class MockSession:
    def __init__(self, data=None):
        self.data = data
        self.committed = False
        self.added = []
        self.refreshed = []
        self.deleted = False
    async def execute(self, stmt):
        return MockResult(self.data)
    async def commit(self):
        self.committed = True
    async def refresh(self, obj):
        self.refreshed.append(obj)
    def add(self, obj):
        self.added.append(obj)

@pytest.fixture
def mock_request():
    req = Mock(spec=Request)
    req.state.db = MockSession()
    return req
