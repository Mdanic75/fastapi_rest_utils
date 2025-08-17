"""SQLAlchemy viewsets for fastapi-rest-utils."""

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, TypeVar

from fastapi import HTTPException, Request, status
from sqlalchemy import delete as sa_delete
from sqlalchemy import select
from sqlalchemy import update as sa_update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.elements import Sequence

from fastapi_rest_utils.viewsets.base import BaseView, CreateView, DeleteView, ListView, RetrieveView, UpdateView

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
PrimaryKeyType = TypeVar("PrimaryKeyType", bound=Any)


class SQLAlchemyBaseView(BaseView):
    """Base SQLAlchemy view that requires a model attribute."""

    @property
    @abstractmethod
    def model(self) -> type[ModelType]:
        """Return the SQLAlchemy model class."""
        ...


class SQLAlchemyListView(SQLAlchemyBaseView, ListView):
    """SQLAlchemy implementation of ListView. Requires 'model' attribute to be set."""

    async def get_objects(self, request: Request) -> Sequence[ModelType]:
        """Get all objects from the database."""
        db: AsyncSession = request.state.db
        stmt = select(self.model)
        result = await db.execute(stmt)
        return result.scalars().all()


class SQLAlchemyRetrieveView(SQLAlchemyBaseView, RetrieveView):
    """SQLAlchemy implementation of RetrieveView."""

    async def get_object(self, request: Request, pk: PrimaryKeyType) -> ModelType:
        """Get a single object by ID from the database."""
        db: AsyncSession = request.state.db
        stmt = select(self.model).where(self.model.id == pk)  # type: ignore[attr-defined]
        result = await db.execute(stmt)
        obj: ModelType | None = result.scalar_one_or_none()
        if obj is None:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj


class SQLAlchemyCreateView(SQLAlchemyBaseView, CreateView):
    """SQLAlchemy implementation of CreateView."""

    async def create_object(self, request: Request, payload: dict) -> ModelType:
        """Create a new object in the database."""
        db: AsyncSession = request.state.db
        obj = self.model(**payload)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj  # type: ignore[return-value]


class SQLAlchemyUpdateView(SQLAlchemyBaseView, UpdateView):
    """SQLAlchemy implementation of UpdateView."""

    async def update_object(self, request: Request, pk: PrimaryKeyType, payload: dict) -> ModelType:
        """Update an object by ID in the database."""
        db: AsyncSession = request.state.db
        stmt = sa_update(self.model).where(self.model.id == pk).values(**payload).returning(self.model)  # type: ignore[attr-defined]
        result = await db.execute(stmt)
        obj: ModelType | None = result.scalar_one_or_none()
        if obj is None:
            raise HTTPException(status_code=404, detail="Object not found")
        await db.commit()
        return obj


class SQLAlchemyDeleteView(SQLAlchemyBaseView, DeleteView):
    """SQLAlchemy implementation of DeleteView."""

    async def delete_object(self, request: Request, pk: PrimaryKeyType) -> dict[str, int]:
        """Delete an object by ID from the database."""
        db: AsyncSession = request.state.db
        stmt = sa_delete(self.model).where(self.model.id == pk)  # type: ignore[attr-defined]
        await db.execute(stmt)
        await db.commit()
        return {"status": status.HTTP_204_NO_CONTENT}


class ModelViewSet(
    SQLAlchemyListView,
    SQLAlchemyRetrieveView,
    SQLAlchemyCreateView,
    SQLAlchemyUpdateView,
    SQLAlchemyDeleteView,
):
    """SQLAlchemy implementation of ModelViewSet."""
