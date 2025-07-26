# FastAPI REST Utils

A collection of utilities for building REST APIs with FastAPI, providing viewset-based API development with SQLAlchemy integration.

## 🚀 Features

- **ViewSet Base Classes**: Abstract base classes for building RESTful viewsets with full CRUD operations
- **SQLAlchemy Integration**: Built-in support for SQLAlchemy models with async/await patterns
- **Router Utilities**: Extended APIRouter with viewset registration capabilities
- **Dependency Injection**: Common dependency injection patterns for FastAPI
- **Type Safety**: Full type hints and Pydantic integration

## 📦 Installation

```bash
pip install fastapi-rest-utils
```

## 🏃‍♂️ Quick Start

```python
from fastapi import FastAPI, Depends
from fastapi_rest_utils.viewsets.sqlalchemy import ModelViewSet
from fastapi_rest_utils.router import RestRouter
from fastapi_rest_utils.deps import db_dep_injector
from pydantic import BaseModel

# Define schemas
class ProductBase(BaseModel):
    name: str
    price: float

class ProductResponse(ProductBase):
    id: int

# Define SQLAlchemy model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

# Create viewset
class ProductViewSet(ModelViewSet):
    model = Product
    schema_config = {
        "list": {"response": list[ProductResponse]},
        "retrieve": {"response": ProductResponse},
        "create": {"payload": ProductBase, "response": ProductResponse},
        "update": {"payload": ProductBase, "response": ProductResponse},
    }

# Register with router
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

## 📚 Core Concepts

### ViewSets

ViewSets combine multiple views (list, retrieve, create, update, delete) into a single class and automatically generate routes.

#### Available Views
- **ListView**: GET requests to list all objects
- **RetrieveView**: GET requests to retrieve a single object
- **CreateView**: POST requests to create new objects
- **UpdateView**: PUT requests to update objects
- **DeleteView**: DELETE requests to remove objects

### Schema Configuration

```python
schema_config = {
    "list": {"response": list[ProductResponse]},
    "retrieve": {"response": ProductResponse},
    "create": {"payload": ProductCreate, "response": ProductResponse},
    "update": {"payload": ProductUpdate, "response": ProductResponse},
}
```

### Router Registration

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

Complete CRUD viewset for SQLAlchemy models.

**Required Attributes:**
- `model`: The SQLAlchemy model class
- `schema_config`: Dictionary defining request/response schemas
- `dependency`: List of callable dependencies

**Overridable Methods:**
- `get_objects(request, *args, **kwargs)`: Customize list query logic
- `get_object(request, id, *args, **kwargs)`: Customize single object retrieval
- `create_object(request, payload, *args, **kwargs)`: Customize object creation
- `update_object(request, id, payload, *args, **kwargs)`: Customize object updates
- `delete_object(request, id, *args, **kwargs)`: Customize object deletion

### Dependency Utilities

```python
# Inject database session into request.state.db
dependencies=[Depends(db_dep_injector(get_async_session))]

# Inject authenticated user into request.state.user
dependencies=[Depends(auth_dep_injector(current_active_user))]
```

## 🧪 Testing

```bash
pytest
```

## 📋 Requirements

- Python 3.8+
- FastAPI >= 0.100.0
- Pydantic >= 2.0.0
- SQLAlchemy >= 2.0.0

## 🔮 Future Plans

- **Pagination**: Cursor-based and offset-based pagination
- **Filtration**: Query parameter filtering and complex filter expressions
- **Ordering**: Multi-field sorting with configurable defaults
- **Bulk Operations**: Batch create, update, and delete operations
- **Field Selection**: Allow clients to specify which fields to include/exclude

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details. 