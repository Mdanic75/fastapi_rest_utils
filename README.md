# FastAPI REST Utils

A collection of utilities for building REST APIs with FastAPI, providing common patterns and abstractions for viewset-based API development.

## Features

- **ViewSet Base Classes**: Abstract base classes for building RESTful viewsets
- **Router Utilities**: Helper functions for creating and configuring FastAPI routers
- **Dependency Injection**: Common dependency injection patterns for FastAPI
- **SQLAlchemy Integration**: Utilities for working with SQLAlchemy models
- **Type Safety**: Full type hints and Pydantic integration

## Installation

```bash
pip install fastapi-rest-utils
```

## Quick Start

```python
from fastapi import FastAPI
from fastapi_rest_utils import ViewSet, router_from_viewset
from fastapi_rest_utils.viewsets.sqlalchemy import SQLAlchemyViewSet

# Create your viewset
class ProductViewSet(SQLAlchemyViewSet):
    model = Product
    response_model = ProductResponse
    
    # Define your CRUD operations
    async def list(self) -> dict:
        # Implementation here
        pass

# Create router from viewset
app = FastAPI()
router = router_from_viewset(ProductViewSet, prefix="/products")
app.include_router(router)
```

## Development

To install in development mode:

```bash
pip install -e ".[dev]"
```

## License

MIT License 