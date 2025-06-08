#!/usr/bin/env python3
"""
手動統合テストスクリプト

MCP Inspectorで実行すべきテストケースを自動化し、
実際のMCPサーバーの動作を検証します。
"""

import sys
import traceback
from typing import Dict, Any, List
import time

# テスト対象のインポート
from app.tools.project_tools import (
    create_project_tool,
    get_projects_tool,
    get_project_tool,
    update_project_tool,
    delete_project_tool
)
from app.tools.user_tools import (
    create_user_tool,
    get_users_tool,
    get_user_tool
)
from app.tools.task_tools import (
    create_task_tool,
    get_tasks_tool,
    get_task_tool,
    update_task_tool,
    delete_task_tool
)
from app.tools.message_tools import (
    create_message_tool,
    get_messages_tool,
    get_message_tool
)
from app.resources.project_resources import project_resource_handler
from app.resources.task_resources import task_resource_handler
from app.resources.user_resources import user_resource_handler
from app.resources.message_resources import messages_recent_resource_handler
from app.db.database import init_db


class IntegrationTestRunner:
    """統合テスト実行クラス"""
    
    def __init__(self):
        self.test_data = {}
        self.passed_tests = 0
        self.failed_tests = 0
        self.errors = []
        # ユニークサフィックスを生成
        self.unique_suffix = str(int(time.time()))
    
    def log_success(self, test_name: str, message: str = ""):
        """成功ログ"""
        print(f"✅ {test_name}: PASSED {message}")
        self.passed_tests += 1
    
    def log_error(self, test_name: str, error: Exception):
        """エラーログ"""
        print(f"❌ {test_name}: FAILED - {str(error)}")
        self.failed_tests += 1
        self.errors.append(f"{test_name}: {str(error)}")
    
    def run_test(self, test_name: str, test_func):
        """個別テスト実行"""
        try:
            result = test_func()
            if result:
                self.log_success(test_name, f"- {result}")
            else:
                self.log_success(test_name)
        except Exception as e:
            self.log_error(test_name, e)
            traceback.print_exc()
    
    def test_01_database_initialization(self):
        """データベース初期化テスト"""
        init_db()
        return "Database initialized successfully"
    
    def test_02_project_creation(self):
        """プロジェクト作成テスト"""
        project = create_project_tool(
            name=f"Integration Test Project {self.unique_suffix}",
            description="Test project for integration testing"
        )
        
        assert "id" in project
        assert project["name"] == f"Integration Test Project {self.unique_suffix}"
        assert project["description"] == "Test project for integration testing"
        assert "created_at" in project
        assert "updated_at" in project
        
        self.test_data["project_id"] = project["id"]
        self.test_data["project_name"] = project["name"]
        return f"Project created with ID: {project['id']}"
    
    def test_03_user_creation(self):
        """ユーザー作成テスト"""
        user = create_user_tool(
            username=f"integration_test_user_{self.unique_suffix}",
            email=f"integration_{self.unique_suffix}@test.com"
        )
        
        assert "id" in user
        assert user["username"] == f"integration_test_user_{self.unique_suffix}"
        assert user["email"] == f"integration_{self.unique_suffix}@test.com"
        assert "created_at" in user
        assert "updated_at" in user
        
        self.test_data["user_id"] = user["id"]
        self.test_data["username"] = user["username"]
        return f"User created with ID: {user['id']}"
    
    def test_04_task_creation(self):
        """タスク作成テスト"""
        project_id = self.test_data["project_id"]
        user_id = self.test_data["user_id"]
        
        task = create_task_tool(
            title="Integration Test Task",
            project_id=project_id,
            description="Test task for integration testing",
            status="pending",
            assignee_id=user_id
        )
        
        assert "id" in task
        assert task["title"] == "Integration Test Task"
        assert task["project_id"] == project_id
        assert task["assignee_id"] == user_id
        assert task["status"] == "pending"
        
        self.test_data["task_id"] = task["id"]
        return f"Task created with ID: {task['id']}"
    
    def test_05_message_creation(self):
        """メッセージ作成テスト"""
        user_id = self.test_data["user_id"]
        project_id = self.test_data["project_id"]
        task_id = self.test_data["task_id"]
        
        message = create_message_tool(
            content="Integration test message",
            message_type="status_update",
            user_id=user_id,
            project_id=project_id,
            task_id=task_id
        )
        
        assert "id" in message
        assert message["content"] == "Integration test message"
        assert message["user_id"] == user_id
        assert message["project_id"] == project_id
        assert message["task_id"] == task_id
        
        self.test_data["message_id"] = message["id"]
        return f"Message created with ID: {message['id']}"
    
    def test_06_project_retrieval(self):
        """プロジェクト取得テスト"""
        project_id = self.test_data["project_id"]
        
        # 単一プロジェクト取得
        project = get_project_tool(project_id)
        assert project["id"] == project_id
        assert project["name"] == f"Integration Test Project {self.unique_suffix}"
        
        # 全プロジェクト取得
        projects = get_projects_tool()
        assert len(projects) > 0
        assert any(p["id"] == project_id for p in projects)
        
        return f"Project retrieval successful, total projects: {len(projects)}"
    
    def test_07_user_retrieval(self):
        """ユーザー取得テスト"""
        user_id = self.test_data["user_id"]
        
        # 単一ユーザー取得
        user = get_user_tool(user_id)
        assert user["id"] == user_id
        assert user["username"] == f"integration_test_user_{self.unique_suffix}"
        
        # 全ユーザー取得
        users = get_users_tool()
        assert len(users) > 0
        assert any(u["id"] == user_id for u in users)
        
        return f"User retrieval successful, total users: {len(users)}"
    
    def test_08_task_retrieval_and_filtering(self):
        """タスク取得・フィルタリングテスト"""
        task_id = self.test_data["task_id"]
        project_id = self.test_data["project_id"]
        user_id = self.test_data["user_id"]
        
        # 単一タスク取得
        task = get_task_tool(task_id)
        assert task["id"] == task_id
        assert task["title"] == "Integration Test Task"
        
        # プロジェクトフィルタリング
        project_tasks = get_tasks_tool(project_id=project_id)
        assert any(t["id"] == task_id for t in project_tasks)
        
        # ステータスフィルタリング
        pending_tasks = get_tasks_tool(status="pending")
        assert any(t["id"] == task_id for t in pending_tasks)
        
        # 担当者フィルタリング
        user_tasks = get_tasks_tool(assignee_id=user_id)
        assert any(t["id"] == task_id for t in user_tasks)
        
        return f"Task filtering successful, project tasks: {len(project_tasks)}"
    
    def test_09_message_retrieval_and_filtering(self):
        """メッセージ取得・フィルタリングテスト"""
        message_id = self.test_data["message_id"]
        project_id = self.test_data["project_id"]
        task_id = self.test_data["task_id"]
        user_id = self.test_data["user_id"]
        
        # 単一メッセージ取得
        message = get_message_tool(message_id)
        assert message["id"] == message_id
        assert message["content"] == "Integration test message"
        
        # プロジェクトフィルタリング
        project_messages = get_messages_tool(project_id=project_id)
        assert any(m["id"] == message_id for m in project_messages)
        
        # タスクフィルタリング
        task_messages = get_messages_tool(task_id=task_id)
        assert any(m["id"] == message_id for m in task_messages)
        
        # ユーザーフィルタリング
        user_messages = get_messages_tool(user_id=user_id)
        assert any(m["id"] == message_id for m in user_messages)
        
        return f"Message filtering successful, project messages: {len(project_messages)}"
    
    def test_10_resource_handlers(self):
        """リソースハンドラーテスト"""
        project_id = self.test_data["project_id"]
        task_id = self.test_data["task_id"]
        user_id = self.test_data["user_id"]
        
        # プロジェクトリソース（タスク含む）
        project_resource = project_resource_handler(
            project_id=str(project_id),
            include_tasks=True
        )
        assert project_resource["id"] == project_id
        assert "tasks" in project_resource
        assert len(project_resource["tasks"]) > 0
        
        # タスクリソース
        task_resource = task_resource_handler(task_id=str(task_id))
        assert task_resource["id"] == task_id
        assert task_resource["project_id"] == project_id
        
        # ユーザーリソース
        user_resource = user_resource_handler(user_identifier=user_id)
        assert user_resource["id"] == user_id
        assert user_resource["username"] == f"integration_test_user_{self.unique_suffix}"
        
        # 最新メッセージリソース
        recent_messages = messages_recent_resource_handler(limit=10)
        assert "messages" in recent_messages
        assert "total_count" in recent_messages
        
        return f"All resource handlers working, recent messages: {recent_messages['total_count']}"
    
    def test_11_update_operations(self):
        """更新操作テスト"""
        project_id = self.test_data["project_id"]
        task_id = self.test_data["task_id"]
        
        # プロジェクト更新
        updated_project = update_project_tool(
            project_id=project_id,
            name=f"Updated Integration Test Project {self.unique_suffix}",
            description="Updated description for testing"
        )
        assert updated_project["name"] == f"Updated Integration Test Project {self.unique_suffix}"
        assert updated_project["description"] == "Updated description for testing"
        
        # タスク更新
        updated_task = update_task_tool(
            task_id=task_id,
            title="Updated Integration Test Task",
            status="in_progress"
        )
        assert updated_task["title"] == "Updated Integration Test Task"
        assert updated_task["status"] == "in_progress"
        
        return "Update operations successful"
    
    def test_12_error_handling(self):
        """エラーハンドリングテスト"""
        error_count = 0
        
        # 存在しないプロジェクト
        try:
            get_project_tool(99999)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Project not found" in str(e)
            error_count += 1
        
        # 存在しないタスク
        try:
            get_task_tool(99999)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Task not found" in str(e)
            error_count += 1
        
        # 存在しないユーザー
        try:
            get_user_tool(99999)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "User not found" in str(e)
            error_count += 1
        
        # 存在しないメッセージ
        try:
            get_message_tool(99999)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Message not found" in str(e)
            error_count += 1
        
        # バリデーションエラー
        try:
            create_project_tool(name="")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Project name is required" in str(e)
            error_count += 1
        
        return f"Error handling working correctly, {error_count} errors caught"
    
    def test_13_cleanup(self):
        """クリーンアップテスト"""
        task_id = self.test_data["task_id"]
        project_id = self.test_data["project_id"]
        
        # タスク削除
        delete_result = delete_task_tool(task_id)
        assert delete_result["success"] is True
        
        # 削除確認
        try:
            get_task_tool(task_id)
            assert False, "Task should have been deleted"
        except ValueError:
            pass  # Expected
        
        # プロジェクト削除
        delete_result = delete_project_tool(project_id)
        assert delete_result["success"] is True
        
        # 削除確認
        try:
            get_project_tool(project_id)
            assert False, "Project should have been deleted"
        except ValueError:
            pass  # Expected
        
        return "Cleanup operations successful"
    
    def run_all_tests(self):
        """全テスト実行"""
        print("🚀 DevLog MCP Server 統合テスト開始")
        print("=" * 60)
        
        # テスト実行
        test_methods = [
            ("Database Initialization", self.test_01_database_initialization),
            ("Project Creation", self.test_02_project_creation),
            ("User Creation", self.test_03_user_creation),
            ("Task Creation", self.test_04_task_creation),
            ("Message Creation", self.test_05_message_creation),
            ("Project Retrieval", self.test_06_project_retrieval),
            ("User Retrieval", self.test_07_user_retrieval),
            ("Task Retrieval & Filtering", self.test_08_task_retrieval_and_filtering),
            ("Message Retrieval & Filtering", self.test_09_message_retrieval_and_filtering),
            ("Resource Handlers", self.test_10_resource_handlers),
            ("Update Operations", self.test_11_update_operations),
            ("Error Handling", self.test_12_error_handling),
            ("Cleanup Operations", self.test_13_cleanup),
        ]
        
        for test_name, test_func in test_methods:
            self.run_test(test_name, test_func)
        
        # 結果サマリー
        print("=" * 60)
        print(f"📊 テスト結果サマリー:")
        print(f"   ✅ 成功: {self.passed_tests}")
        print(f"   ❌ 失敗: {self.failed_tests}")
        print(f"   📈 成功率: {(self.passed_tests / (self.passed_tests + self.failed_tests) * 100):.1f}%")
        
        if self.errors:
            print(f"\n🔍 エラー詳細:")
            for error in self.errors:
                print(f"   - {error}")
        
        if self.failed_tests == 0:
            print("\n🎉 全てのテストが成功しました！MCPサーバーは正常に動作しています。")
            return True
        else:
            print(f"\n⚠️  {self.failed_tests}個のテストが失敗しました。修正が必要です。")
            return False


def main():
    """メイン実行関数"""
    runner = IntegrationTestRunner()
    success = runner.run_all_tests()
    
    # 終了コード設定
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 