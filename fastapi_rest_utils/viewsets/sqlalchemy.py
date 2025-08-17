"""SQLAlchemy viewsets for fastapi-rest-utils."""

from abc import abstractmethod
from typing import Any

from fastapi import Request, status
from sqlalchemy import delete as sa_delete
from sqlalchemy import select
from sqlalchemy import update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseView, CreateView, DeleteView, ListView, RetrieveView, UpdateView


class SQLAlchemyBaseView(BaseView):
    @property
    @abstractmethod
    def model(self) -> Any: ...


class SQLAlchemyListView(SQLAlchemyBaseView, ListView):
    """SQLAlchemy implementation of ListView. Requires 'model' attribute to be set."""

    async def get_objects(self, request: Request) -> Any:
        db: AsyncSession = request.state.db
        stmt = select(self.model)
        result = await db.execute(stmt)
        return result.scalars().all()


class SQLAlchemyRetrieveView(SQLAlchemyBaseView, RetrieveView):
    async def get_object(self, request: Request, id: Any) -> Any:
        db: AsyncSession = request.state.db
        stmt = select(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj is None:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Object not found")
        return obj


class SQLAlchemyCreateView(SQLAlchemyBaseView, CreateView):
    model: Any

    async def create_object(self, request: Request, payload: Any) -> Any:
        db: AsyncSession = request.state.db
        obj = self.model(**payload)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj


class SQLAlchemyUpdateView(SQLAlchemyBaseView, UpdateView):
    async def update_object(self, request: Request, id: Any, payload: Any) -> Any:
        db: AsyncSession = request.state.db
        stmt = sa_update(self.model).where(self.model.id == id).values(**payload).returning(self.model)
        result = await db.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj is None:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Object not found")
        await db.commit()
        return obj


class SQLAlchemyDeleteView(SQLAlchemyBaseView, DeleteView):
    async def delete_object(self, request: Request, id: Any) -> Any:
        db: AsyncSession = request.state.db
        stmt = sa_delete(self.model).where(self.model.id == id)
        await db.execute(stmt)
        await db.commit()
        return {"status": status.HTTP_204_NO_CONTENT}


class ModelViewSet(
    SQLAlchemyListView, SQLAlchemyRetrieveView, SQLAlchemyCreateView, SQLAlchemyUpdateView, SQLAlchemyDeleteView
):
    """SQLAlchemy implementation of ModelViewSet."""
