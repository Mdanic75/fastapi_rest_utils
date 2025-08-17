"""Dependency utilities for fastapi-rest-utils."""

from collections.abc import Callable
from typing import Any

from fastapi import Depends, Request


def db_dep_injector(session_dependency: Callable) -> Callable[[Request], Any]:
    """Return a dependency that attaches the db session to request.state.db.

    Usage:
        dependencies=[Depends(db_dep_injector(get_async_session))]
    Then access in endpoint: db = request.state.db
    """

    async def set_db_on_request(request: Request, db: Any = Depends(session_dependency)) -> None:  # noqa: ANN401
        request.state.db = db

    return set_db_on_request


def auth_dep_injector(user_dependency: Callable) -> Callable[[Request], Any]:
    """Return a dependency that attaches the authenticated user to request.state.user.

    Usage:
        dependencies=[Depends(auth_dep_injector(current_active_user))]
    Then access in endpoint: user = request.state.user
    """

    async def set_user_on_request(request: Request, user: Any = Depends(user_dependency)) -> Any:  # noqa: ANN401
        request.state.user = user
        return user

    return set_user_on_request
