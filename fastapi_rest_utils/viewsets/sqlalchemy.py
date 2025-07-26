"""SQLAlchemy viewsets for fastapi-rest-utils."""
from .base import ListView, RetrieveView, CreateView, UpdateView, PartialUpdateView, DeleteView, BaseViewSet
from fastapi import Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sa_update, delete as sa_delete
from typing import Any, Callable, List


class SQLAlchemyBaseViewSet(BaseViewSet):
    """
    Base SQLAlchemy viewset that requires a model and database dependency.
    Inherit from this class and from any SQLAlchemy view classes (e.g., SQLAlchemyListView, SQLAlchemyRetrieveView, etc.).
    """
    model: Any
    dependency: List[Callable[..., AsyncSession]]


class SQLAlchemyListView(ListView):
    """
    SQLAlchemy implementation of ListView. Requires 'model' attribute to be set.
    """
    model: Any

    async def get_objects(self, request: Request, *args, **kwargs) -> Any:
        db: AsyncSession = request.state.db
        stmt = select(self.model)
        result = await db.execute(stmt)
        return result.scalars().all()

class SQLAlchemyRetrieveView(RetrieveView):
    model: Any

    async def get_object(self, request: Request, id: Any, *args, **kwargs) -> Any:
        db: AsyncSession = request.state.db
        stmt = select(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj is None:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Object not found")
        return obj

class SQLAlchemyCreateView(CreateView):
    model: Any

    async def create_object(self, request: Request, payload: Any, *args, **kwargs) -> Any:
        db: AsyncSession = request.state.db
        obj = self.model(**payload)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

class SQLAlchemyUpdateView(UpdateView):
    model: Any

    async def update_object(self, request: Request, id: Any, payload: Any, *args, **kwargs) -> Any:
        db: AsyncSession = request.state.db
        stmt = sa_update(self.model).where(self.model.id == id).values(**payload).returning(self.model)
        result = await db.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj is None:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Object not found")
        await db.commit()
        return obj

class SQLAlchemyDeleteView(DeleteView):
    model: Any

    async def delete_object(self, request: Request, id: Any, *args, **kwargs) -> Any:
        db: AsyncSession = request.state.db
        stmt = sa_delete(self.model).where(self.model.id == id)
        await db.execute(stmt)
        await db.commit()
        return {"status": status.HTTP_204_NO_CONTENT} 

class ModelViewSet(SQLAlchemyBaseViewSet, ListView, RetrieveView, CreateView, UpdateView, DeleteView):
    """
    SQLAlchemy implementation of ModelViewSet.
    """