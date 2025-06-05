"""
MCP Resources Package

This package contains all MCP resource implementations for DevStatusMCP.
"""

from .project_resources import project_resource_handler

# TODO: 他のリソースファイルが作成されたら、以下のインポートを有効化する
# from .task_resources import task_resource_handler  
# from .user_resources import user_resource_handler
# from .message_resources import messages_recent_resource_handler

__all__ = [
    "project_resource_handler",
    # TODO: 他のリソースが作成されたら、以下を有効化する
    # "task_resource_handler", 
    # "user_resource_handler",
    # "messages_recent_resource_handler",
] 