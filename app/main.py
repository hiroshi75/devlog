"""
DevLog - FastMCP Server for Development Status Management

This module provides the main FastMCP server implementation for DevLog,
a Slack-like development status sharing service.

Features:
- Project and task management
- User management and authentication
- Real-time messaging and status updates
- SQLAlchemy ORM with PostgreSQL/SQLite support
- Comprehensive MCP tools and resources

Usage:
    python -m app.main

Environment Variables:
    DEVLOG_DATABASE_URL: Database connection URL
    DEVLOG_DEBUG: Enable debug mode (default: False)
    DEVLOG_LOG_LEVEL: Logging level (default: INFO)
"""

import logging
import os
from typing import Any, Dict

from fastmcp import FastMCP
from app.db.database import init_db

# Import all tools
from app.tools import (
    # Project tools
    create_project_tool,
    get_projects_tool,
    get_project_tool,
    update_project_tool,
    delete_project_tool,
    # Task tools
    create_task_tool,
    get_tasks_tool,
    get_task_tool,
    update_task_tool,
    delete_task_tool,
    # User tools
    create_user_tool,
    get_users_tool,
    get_user_tool,
    # Message tools
    create_message_tool,
    create_direct_message_tool,
    get_messages_tool,
    get_direct_messages_tool,
    get_thread_messages_tool,
    get_unread_messages_tool,
    get_message_tool,
    mark_message_as_read_tool,
    mark_conversation_as_read_tool,
    delete_message_tool,
)

# Import all resource handlers
from app.resources import (
    project_resource_handler,
    task_resource_handler,
    user_resource_handler,
    messages_recent_resource_handler,
)

# Configure logging
log_level = os.getenv("DEVLOG_LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create FastMCP instance
mcp = FastMCP("DevLog","""
This tool is designed for developers to share updates on their progress, current tasks, and upcoming work — like a lightweight Slack for team coordination.
""")

# Initialize database on startup
init_db()

# Register Project Tools
@mcp.tool()
def create_project(name: str, description: str = None) -> dict:
    """Create a new project"""
    return create_project_tool(name=name, description=description)

@mcp.tool()
def get_projects() -> list:
    """Get all projects"""
    return get_projects_tool()

@mcp.tool()
def get_project(project_id: int) -> dict:
    """Get a specific project by ID"""
    return get_project_tool(project_id=project_id)

@mcp.tool()
def update_project(project_id: int, name: str = None, description: str = None) -> dict:
    """Update a project"""
    return update_project_tool(project_id=project_id, name=name, description=description)

@mcp.tool()
def delete_project(project_id: int) -> dict:
    """Delete a project"""
    return delete_project_tool(project_id=project_id)

# Register Task Tools
@mcp.tool()
def create_task(
    title: str,
    project_id: int,
    description: str = None,
    status: str = "pending",
    assignee_id: int = None
) -> dict:
    """Create a new task"""
    return create_task_tool(
        title=title,
        project_id=project_id,
        description=description,
        status=status,
        assignee_id=assignee_id
    )

@mcp.tool()
def get_tasks(project_id: int = None, status: str = None, assignee_id: int = None) -> list:
    """Get tasks with optional filtering"""
    return get_tasks_tool(project_id=project_id, status=status, assignee_id=assignee_id)

@mcp.tool()
def get_task(task_id: int) -> dict:
    """Get a specific task by ID"""
    return get_task_tool(task_id=task_id)

@mcp.tool()
def update_task(
    task_id: int,
    title: str = None,
    description: str = None,
    status: str = None,
    assignee_id: int = None
) -> dict:
    """Update a task"""
    return update_task_tool(
        task_id=task_id,
        title=title,
        description=description,
        status=status,
        assignee_id=assignee_id
    )

@mcp.tool()
def delete_task(task_id: int) -> dict:
    """Delete a task"""
    return delete_task_tool(task_id=task_id)

# Register User Tools
@mcp.tool()
def create_user(username: str, email: str) -> dict:
    """Create a new user"""
    return create_user_tool(username=username, email=email)

@mcp.tool()
def get_users() -> list:
    """Get all users"""
    return get_users_tool()

@mcp.tool()
def get_user(user_id: int) -> dict:
    """Get a specific user by ID"""
    return get_user_tool(user_id=user_id)

# Register Message Tools
@mcp.tool()
def create_message(
    content: str,
    user_id: int,
    message_type: str = "comment",
    task_id: int = None,
    project_id: int = None,
    parent_id: int = None,
    recipient_id: int = None
) -> dict:
    """Create a new message (including direct messages and threaded replies)"""
    return create_message_tool(
        content=content,
        user_id=user_id,
        message_type=message_type,
        task_id=task_id,
        project_id=project_id,
        parent_id=parent_id,
        recipient_id=recipient_id
    )

@mcp.tool()
def create_direct_message(
    content: str,
    user_id: int,
    recipient_id: int,
    parent_id: int = None
) -> dict:
    """Create a direct message between two users"""
    return create_direct_message_tool(
        content=content,
        user_id=user_id,
        recipient_id=recipient_id,
        parent_id=parent_id
    )

@mcp.tool()
def get_messages(
    project_id: int = None,
    task_id: int = None,
    user_id: int = None,
    recipient_id: int = None,
    message_type: str = None,
    parent_id: int = None,
    include_deleted: bool = False,
    limit: int = 100
) -> list:
    """Get messages with optional filtering"""
    return get_messages_tool(
        project_id=project_id,
        task_id=task_id,
        user_id=user_id,
        recipient_id=recipient_id,
        message_type=message_type,
        parent_id=parent_id,
        include_deleted=include_deleted,
        limit=limit
    )

@mcp.tool()
def get_direct_messages(
    user_id: int,
    other_user_id: int,
    limit: int = 100
) -> list:
    """Get direct messages between two users"""
    return get_direct_messages_tool(
        user_id=user_id,
        other_user_id=other_user_id,
        limit=limit
    )

@mcp.tool()
def get_thread_messages(
    parent_id: int,
    limit: int = 100
) -> list:
    """Get all replies to a specific message (thread)"""
    return get_thread_messages_tool(
        parent_id=parent_id,
        limit=limit
    )

@mcp.tool()
def get_unread_messages(
    user_id: int,
    message_type: str = None
) -> list:
    """Get unread messages for a user"""
    return get_unread_messages_tool(
        user_id=user_id,
        message_type=message_type
    )

@mcp.tool()
def mark_message_as_read(message_id: int) -> dict:
    """Mark a specific message as read"""
    return mark_message_as_read_tool(message_id=message_id)

@mcp.tool()
def mark_conversation_as_read(user_id: int, other_user_id: int) -> dict:
    """Mark all messages in a conversation as read"""
    return mark_conversation_as_read_tool(
        user_id=user_id,
        other_user_id=other_user_id
    )

@mcp.tool()
def delete_message(message_id: int) -> dict:
    """Delete a message (soft delete)"""
    return delete_message_tool(message_id=message_id)

@mcp.tool()
def get_message(message_id: int) -> dict:
    """Get a specific message by ID"""
    return get_message_tool(message_id=message_id)

# Register Resources
@mcp.resource("project://{project_id}")
def project_resource(project_id: str) -> str:
    """Get project information and optionally related tasks"""
    result = project_resource_handler(project_id=project_id, include_tasks=True)
    return f"Project: {result['name']}\nDescription: {result.get('description', 'No description')}\n\nTasks: {len(result.get('tasks', []))} tasks"

@mcp.resource("task://{task_id}")
def task_resource(task_id: str) -> str:
    """Get task information"""
    result = task_resource_handler(task_id=task_id)
    return f"Task: {result['title']}\nStatus: {result['status']}\nDescription: {result.get('description', 'No description')}"

@mcp.resource("user://{user_id}")
def user_resource(user_id: str) -> str:
    """Get user information"""
    result = user_resource_handler(user_id=user_id)
    return f"User: {result['username']}\nEmail: {result['email']}"

@mcp.resource("messages://{type}")
def messages_resource(type: str) -> str:
    """Get messages by type (e.g., recent, all, etc.)"""
    if type == "recent":
        result = messages_recent_resource_handler(limit=20)
        messages = result.get('messages', [])
        
        if not messages:
            return "Recent Messages:\n\nNo messages found."
        
        messages_text = "\n".join([
            f"[{msg['created_at']}] {msg['user_id']}: {msg['content']}"
            for msg in messages
        ])
        return f"Recent Messages:\n\n{messages_text}"
    else:
        return f"Message type '{type}' is not supported. Available types: recent"

if __name__ == "__main__":
    mcp.run()