"""
Tests for the main FastMCP server implementation
"""

import pytest
from fastmcp import FastMCP
from unittest.mock import patch, MagicMock


def test_mcp_server_creation():
    """Test that MCP server can be created"""
    from app.main import mcp
    
    assert isinstance(mcp, FastMCP)
    assert mcp.name == "DevStatusMCP"


@pytest.mark.asyncio
async def test_mcp_server_has_required_tools():
    """Test that all required tools are registered"""
    from app.main import mcp
    
    # Get tools dictionary from registered tools
    tools = await mcp.get_tools()
    tool_names = list(tools.keys())
    
    # Project tools
    assert "create_project" in tool_names
    assert "get_projects" in tool_names
    assert "get_project" in tool_names
    assert "update_project" in tool_names
    assert "delete_project" in tool_names
    
    # Task tools
    assert "create_task" in tool_names
    assert "get_tasks" in tool_names
    assert "get_task" in tool_names
    assert "update_task" in tool_names
    assert "delete_task" in tool_names
    
    # User tools
    assert "create_user" in tool_names
    assert "get_users" in tool_names
    assert "get_user" in tool_names
    
    # Message tools
    assert "create_message" in tool_names
    assert "get_messages" in tool_names
    assert "get_message" in tool_names


@pytest.mark.asyncio
async def test_mcp_server_has_required_resources():
    """Test that all required resources are registered"""
    from app.main import mcp
    
    # Get resource templates dictionary from registered resources
    resource_templates = await mcp.get_resource_templates()
    resource_uris = list(resource_templates.keys())
    
    assert any("project://" in uri for uri in resource_uris)
    assert any("task://" in uri for uri in resource_uris)
    assert any("user://" in uri for uri in resource_uris)
    assert any("messages://" in uri for uri in resource_uris)
    
    # Specifically check for messages://{type} pattern
    assert "messages://{type}" in resource_uris


def test_create_project_tool_direct():
    """Test that create_project tool works directly"""
    with patch('app.tools.project_tools.get_db') as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value.__next__ = MagicMock(return_value=mock_db)
        
        # Mock crud operation
        with patch('app.crud.project.create_project') as mock_create:
            mock_project = MagicMock()
            mock_project.id = 1
            mock_project.name = "Test Project"
            mock_project.description = "Test Description"
            mock_project.created_at = None
            mock_project.updated_at = None
            mock_create.return_value = mock_project
            
            # Import and call the tool function directly
            from app.main import create_project
            result = create_project(name="Test Project", description="Test Description")
            
            assert result["id"] == 1
            assert result["name"] == "Test Project"
            assert result["description"] == "Test Description"


def test_messages_resource_direct():
    """Test that messages_resource works directly"""
    with patch('app.resources.messages_recent_resource_handler') as mock_handler:
        mock_handler.return_value = {
            'messages': [],
            'total_count': 0,
            'limit': 20
        }
        
        # Import and call the resource function directly
        from app.main import messages_resource
        result = messages_resource(type="recent")
        
        assert "Recent Messages:" in result
        assert "No messages found." in result


def test_mcp_server_can_run():
    """Test that MCP server can be started"""
    with patch('fastmcp.FastMCP.run') as mock_run:
        from app.main import mcp
        
        # This should not raise an exception
        assert hasattr(mcp, 'run')
        
        # Test that we can call run (mock prevents actual execution)
        mcp.run()
        mock_run.assert_called_once() 