import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi import Request, Depends

from fastapi_rest_utils.deps import db_dep_injector, auth_dep_injector


class TestDependencyInjectors:
    """Test cases for dependency injectors"""

    
    @pytest.mark.asyncio
    async def test_db_dep_injector_returns_function(self) -> None:
        """Test that db_dep_injector returns a callable function"""
        mock_session_dep = Mock()
        injector = db_dep_injector(mock_session_dep)
        
        # Verify it returns a callable
        assert callable(injector)
        
        # Verify the function signature includes Request and Depends
        import inspect
        sig = inspect.signature(injector)
        assert 'request' in sig.parameters
        assert 'db' in sig.parameters
    
    @pytest.mark.asyncio
    async def test_auth_dep_injector_returns_function(self) -> None:
        """Test that auth_dep_injector returns a callable function"""
        mock_user_dep = Mock()
        injector = auth_dep_injector(mock_user_dep)
        
        # Verify it returns a callable
        assert callable(injector)
        
        # Verify the function signature includes Request and Depends
        import inspect
        sig = inspect.signature(injector)
        assert 'request' in sig.parameters
        assert 'user' in sig.parameters
