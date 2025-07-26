"""Dependency utilities for fastapi-rest-utils."""
from fastapi import Request, Depends


def db_dep_injector(session_dependency):
    """
    Returns a dependency that attaches the db session to request.state.db.
    Usage:
        dependencies=[Depends(db_dep_injector(get_async_session))]
    Then access in endpoint: db = request.state.db
    """
    async def set_db_on_request(request: Request, db=Depends(session_dependency)):
        request.state.db = db
    return set_db_on_request


def auth_dep_injector(user_dependency):
    """
    Returns a dependency that attaches the authenticated user to request.state.user.
    Usage:
        dependencies=[Depends(auth_dep_injector(current_active_user))]
    Then access in endpoint: user = request.state.user
    """
    async def set_user_on_request(request: Request, user=Depends(user_dependency)):
        request.state.user = user
        return user
    return set_user_on_request

