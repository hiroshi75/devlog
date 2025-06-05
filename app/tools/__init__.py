"""
MCP Tools Package for DevLog

This package contains all MCP tool implementations for DevLog.
"""

from .project_tools import (
    create_project_tool,
    get_projects_tool,
    get_project_tool,
    update_project_tool,
    delete_project_tool,
)
from .task_tools import (
    create_task_tool,
    get_tasks_tool,
    get_task_tool,
    update_task_tool,
    delete_task_tool,
)
from .user_tools import (
    create_user_tool,
    get_users_tool,
    get_user_tool,
)
from .message_tools import (
    create_message_tool,
    get_messages_tool,
    get_message_tool,
)

__all__ = [
    # Project tools
    "create_project_tool",
    "get_projects_tool",
    "get_project_tool",
    "update_project_tool",
    "delete_project_tool",
    # Task tools
    "create_task_tool",
    "get_tasks_tool",
    "get_task_tool",
    "update_task_tool",
    "delete_task_tool",
    # User tools
    "create_user_tool",
    "get_users_tool",
    "get_user_tool",
    # Message tools
    "create_message_tool",
    "get_messages_tool",
    "get_message_tool",
] 