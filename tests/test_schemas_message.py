"""
Messageスキーマのテスト

MessageBase, MessageCreate, Messageスキーマの
バリデーションと動作をテストします。
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from app.schemas.message import MessageBase, MessageCreate, Message, MessageType


class TestMessageType:
    """MessageType列挙型のテスト"""
    
    def test_message_type_values(self):
        """メッセージタイプの値を確認"""
        assert MessageType.STATUS_UPDATE == "status_update"
        assert MessageType.COMMENT == "comment"
        assert MessageType.QUESTION == "question"
        assert MessageType.ANSWER == "answer"
        assert MessageType.ANNOUNCEMENT == "announcement"


class TestMessageBase:
    """MessageBaseスキーマのテスト"""
    
    def test_valid_message_base(self):
        """有効なMessageBaseの作成"""
        message = MessageBase(
            content="This is a test message",
            message_type=MessageType.COMMENT,
            user_id=1,
            project_id=1,
            task_id=1,
            parent_id=None
        )
        assert message.content == "This is a test message"
        assert message.message_type == MessageType.COMMENT
        assert message.user_id == 1
        assert message.project_id == 1
        assert message.task_id == 1
        assert message.parent_id is None
    
    def test_message_base_without_optional_fields(self):
        """オプションフィールドなしのMessageBase"""
        message = MessageBase(
            content="Test message",
            message_type=MessageType.STATUS_UPDATE,
            user_id=1,
            project_id=1
        )
        assert message.content == "Test message"
        assert message.message_type == MessageType.STATUS_UPDATE
        assert message.user_id == 1
        assert message.project_id == 1
        assert message.task_id is None
        assert message.parent_id is None
    
    def test_message_base_empty_content(self):
        """空のコンテンツでエラー"""
        with pytest.raises(ValidationError):
            MessageBase(
                content="",
                message_type=MessageType.COMMENT,
                user_id=1,
                project_id=1
            )
    
    def test_message_base_invalid_message_type(self):
        """無効なメッセージタイプでエラー"""
        with pytest.raises(ValidationError):
            MessageBase(
                content="Test message",
                message_type="invalid_type",
                user_id=1,
                project_id=1
            )
    
    def test_message_base_missing_required_fields(self):
        """必須フィールドなしでエラー"""
        with pytest.raises(ValidationError):
            MessageBase(content="Test message")


class TestMessageCreate:
    """MessageCreateスキーマのテスト"""
    
    def test_valid_message_create(self):
        """有効なMessageCreateの作成"""
        message = MessageCreate(
            content="Creating a new message",
            message_type=MessageType.ANNOUNCEMENT,
            user_id=1,
            project_id=1
        )
        assert message.content == "Creating a new message"
        assert message.message_type == MessageType.ANNOUNCEMENT
        assert message.user_id == 1
        assert message.project_id == 1
    
    def test_message_create_inherits_from_base(self):
        """MessageBaseを継承していることを確認"""
        assert issubclass(MessageCreate, MessageBase)


class TestMessage:
    """Messageレスポンススキーマのテスト"""
    
    def test_valid_message_response(self):
        """有効なMessageレスポンスの作成"""
        now = datetime.now()
        message = Message(
            id=1,
            content="Test message",
            message_type=MessageType.COMMENT,
            user_id=1,
            project_id=1,
            task_id=2,
            parent_id=None,
            created_at=now
        )
        assert message.id == 1
        assert message.content == "Test message"
        assert message.message_type == MessageType.COMMENT
        assert message.user_id == 1
        assert message.project_id == 1
        assert message.task_id == 2
        assert message.parent_id is None
        assert message.created_at == now
    
    def test_message_inherits_from_base(self):
        """MessageBaseを継承していることを確認"""
        assert issubclass(Message, MessageBase)
    
    def test_message_from_orm_mode(self):
        """ORMモードが有効であることを確認"""
        assert hasattr(Message, 'model_config')
        assert Message.model_config.get('from_attributes', False) is True 