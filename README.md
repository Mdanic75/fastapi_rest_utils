# FastAPI REST Utils

A comprehensive collection of utilities for building REST APIs with FastAPI, providing common patterns and abstractions for viewset-based API development. This package simplifies the creation of CRUD operations and RESTful endpoints with built-in SQLAlchemy integration, dependency injection utilities, and type-safe schemas.

## 🚀 Features

- **ViewSet Base Classes**: Abstract base classes for building RESTful viewsets with full CRUD operations
- **SQLAlchemy Integration**: Built-in support for SQLAlchemy models with async/await patterns
- **Router Utilities**: Extended APIRouter with viewset registration capabilities
- **Dependency Injection**: Common dependency injection patterns for FastAPI
- **Type Safety**: Full type hints and Pydantic integration for robust API development
- **Flexible Schema Configuration**: Dynamic schema configuration for different operations
- **OpenAPI Integration**: Automatic OpenAPI schema generation with proper documentation

## 📦 Installation

```bash
pip install fastapi-rest-utils
```

For development installation:

```bash
pip install -e ".[dev]"
```

## 🏃‍♂️ Quick Start

### Basic Usage

```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_rest_utils.viewsets.sqlalchemy import ModelViewSet
from fastapi_rest_utils.router import RestRouter
from fastapi_rest_utils.deps import db_dep_injector
from pydantic import BaseModel

# Define your Pydantic schemas
class ProductBase(BaseModel):
    name: str
    price: float

class ProductResponse(ProductBase):
    id: int

# Define your SQLAlchemy model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

# Create your viewset
class ProductViewSet(ModelViewSet):
    model = Product
    schema_config = {
        "list": {"response": list[ProductResponse]},
        "retrieve": {"response": ProductResponse},
        "create": {"payload": ProductBase, "response": ProductResponse},
        "update": {"payload": ProductBase, "response": ProductResponse},
    }

# Create router and register viewset
app = FastAPI()
router = RestRouter()

router.register_viewset(
    viewset=ProductViewSet,
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(db_dep_injector(get_async_session))]
)

app.include_router(router)
```

### Advanced Usage with Custom Logic

```python
from fastapi import Request
from fastapi_rest_utils.viewsets.sqlalchemy import ModelViewSet
from sqlalchemy import select

class ProductViewSet(ModelViewSet):
    model = Product
    schema_config = {
        "list": {"response": list[ProductResponse]},
        "retrieve": {"response": ProductResponse},
        "create": {"payload": ProductBase, "response": ProductResponse},
    }

    async def get_objects(self, request: Request, *args, **kwargs):
        # Custom filtering logic
        db = request.state.db
        stmt = select(self.model).where(self.model.price > 0)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def create_object(self, request: Request, payload: dict, *args, **kwargs):
        # Custom creation logic
        db = request.state.db
        payload["created_by"] = request.state.user.id
        obj = self.model(**payload)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
```

## 📚 Core Concepts

### ViewSets

ViewSets are the core abstraction in fastapi_rest_utils. They combine multiple views (list, retrieve, create, update, delete) into a single class and automatically generate the appropriate routes.

#### Available View Classes

- **ListView**: Handles GET requests to list all objects
- **RetrieveView**: Handles GET requests to retrieve a single object
- **CreateView**: Handles POST requests to create new objects
- **UpdateView**: Handles PUT requests to update objects
- **PartialUpdateView**: Handles PATCH requests for partial updates
- **DeleteView**: Handles DELETE requests to remove objects

#### SQLAlchemy View Classes

- **SQLAlchemyListView**: SQLAlchemy implementation of ListView
- **SQLAlchemyRetrieveView**: SQLAlchemy implementation of RetrieveView
- **SQLAlchemyCreateView**: SQLAlchemy implementation of CreateView
- **SQLAlchemyUpdateView**: SQLAlchemy implementation of UpdateView
- **SQLAlchemyDeleteView**: SQLAlchemy implementation of DeleteView
- **ModelViewSet**: Complete CRUD viewset with all SQLAlchemy operations

### Schema Configuration

The `schema_config` attribute defines the Pydantic models used for different operations:

```python
schema_config = {
    "list": {"response": list[ProductResponse]},
    "retrieve": {"response": ProductResponse},
    "create": {"payload": ProductCreate, "response": ProductResponse},
    "update": {"payload": ProductUpdate, "response": ProductResponse},
    "partial_update": {"payload": ProductPartialUpdate, "response": ProductResponse},
    "destroy": {"response": None},  # No response for delete operations
}
```

### Router Registration

The `RestRouter` extends FastAPI's `APIRouter` with viewset registration capabilities:

```python
router = RestRouter()
router.register_viewset(
    viewset=ProductViewSet,
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(db_dep_injector(get_async_session))]
)
```

## 🔧 API Reference

### ModelViewSet

The most commonly used viewset that provides full CRUD operations for SQLAlchemy models.

```python
class ModelViewSet(SQLAlchemyBaseViewSet, ListView, RetrieveView, CreateView, UpdateView, DeleteView):
    """
    Complete CRUD viewset for SQLAlchemy models.
    
    Attributes:
        model: The SQLAlchemy model class
        schema_config: Configuration for request/response schemas
        dependency: List of dependencies (typically database session)
    """
```

#### Required Attributes

- **model**: The SQLAlchemy model class to operate on
- **schema_config**: Dictionary defining request/response schemas for each operation
- **dependency**: List of callable dependencies (typically database session)

#### Overridable Methods

- `get_objects(request, *args, **kwargs)`: Customize list query logic
- `get_object(request, id, *args, **kwargs)`: Customize single object retrieval
- `create_object(request, payload, *args, **kwargs)`: Customize object creation
- `update_object(request, id, payload, *args, **kwargs)`: Customize object updates
- `delete_object(request, id, *args, **kwargs)`: Customize object deletion

### RestRouter

Extended APIRouter with viewset registration capabilities.

```python
class RestRouter(APIRouter):
    def register_viewset(
        self, 
        viewset_class: Type[BaseViewSetProtocol], 
        prefix: str, 
        tags: Optional[List[str]] = None,
        **kwargs
    ) -> None:
        """
        Register a viewset's routes with this router.
        
        Args:
            viewset_class: The viewset class containing route configurations
            prefix: URL prefix for the viewset routes
            tags: Tags for API documentation
            **kwargs: Additional arguments passed to add_api_route
        """
```

### Dependency Utilities

#### db_dep_injector

Injects database session into request state for easy access in viewsets.

```python
def db_dep_injector(session_dependency):
    """
    Returns a dependency that attaches the db session to request.state.db.
    
    Usage:
        dependencies=[Depends(db_dep_injector(get_async_session))]
    Then access in endpoint: db = request.state.db
    """
```

#### auth_dep_injector

Injects authenticated user into request state.

```python
def auth_dep_injector(user_dependency):
    """
    Returns a dependency that attaches the authenticated user to request.state.user.
    
    Usage:
        dependencies=[Depends(auth_dep_injector(current_active_user))]
    Then access in endpoint: user = request.state.user
    """
```

## 🎯 Advanced Usage Examples


## 🧪 Testing

The package includes comprehensive test coverage. To run tests:

```bash
pytest
```

For development with coverage:

```bash
pytest --cov=fastapi_rest_utils --cov-report=html
```

### Testing ViewSets

```python
import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import Request
from fastapi_rest_utils.viewsets.sqlalchemy import ModelViewSet

class TestProductViewSet:
    @pytest.fixture
    def mock_request(self):
        req = Mock(spec=Request)
        req.state.db = MockSession()
        return req

    async def test_list_products(self, mock_request):
        viewset = ProductViewSet()
        result = await viewset.list(mock_request)
        assert len(result) > 0
```

## 🔍 Type Safety

The package is fully typed with mypy support. All classes implement proper protocols and type hints:

```python
from typing import Protocol, Any, List
from fastapi_rest_utils.protocols import BaseViewSetProtocol

class BaseViewSetProtocol(Protocol):
    """
    Protocol for base viewsets requiring routes_config and dependency.
    """
    dependency: List[Callable[..., Any]]
    def routes_config(self) -> List[RouteConfigDict]: ...
```

## 📋 Requirements

- Python 3.8+
- FastAPI >= 0.100.0
- Pydantic >= 2.0.0
- SQLAlchemy >= 2.0.0
- typing-extensions >= 4.0.0

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/fastapi-rest-utils/issues)
- **Documentation**: This README and inline code documentation
- **Examples**: Check the `tests/` directory for usage examples

## 🔄 Changelog

### v0.1.0
- Initial release
- Basic ViewSet functionality
- SQLAlchemy integration
- Router utilities
- Dependency injection helpers
- Full type safety support 