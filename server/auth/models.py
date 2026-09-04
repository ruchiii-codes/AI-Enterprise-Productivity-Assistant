from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    JSON,
)

from sqlalchemy.orm import relationship

from server.auth.database import Base

from sqlalchemy import DateTime
from datetime import datetime

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    username = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password = Column(
        String,
        nullable=False,
    )

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    verification_token = Column(
        String,
        nullable=True,
    )

    verification_token_expires = Column(
        DateTime,
        nullable=True,
    )

    documents = relationship(
        "Document",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    conversations = relationship(
        "Conversation",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    github_connection = relationship(
        "GitHubConnection",
        back_populates="owner",
        uselist=False,
        cascade="all, delete-orphan",
    )

    gmail_connection = relationship(
        "GmailConnection",
        back_populates="owner",
        uselist=False,
        cascade="all, delete-orphan",
    )

    calendar_connection = relationship(
        "CalendarConnection",
        back_populates="owner",
        uselist=False,
        cascade="all, delete-orphan",
    )

class GitHubConnection(Base):

    __tablename__ = "github_connections"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    github_user_id = Column(
        Integer,
        nullable=False,
    )

    github_username = Column(
        String,
        nullable=False,
    )

    access_token = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="github_connection",
    )    

class GmailConnection(Base):

    __tablename__ = "gmail_connections"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    gmail_email = Column(
        String,
        nullable=False,
    )

    access_token = Column(
        String,
        nullable=False,
    )

    refresh_token = Column(
        String,
        nullable=False,
    )

    token_uri = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="gmail_connection",
    )    

class CalendarConnection(Base):

    __tablename__ = "calendar_connections"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    calendar_email = Column(
        String,
        nullable=False,
    )

    access_token = Column(
        String,
        nullable=False,
    )

    refresh_token = Column(
        String,
        nullable=False,
    )

    token_uri = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="calendar_connection",
    )

class Document(Base):

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    filename = Column(
        String,
        nullable=False,
    )

    file_path = Column(
        String,
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=True,
    )

    page_count = Column(
        Integer,
        nullable=True,
    )

    owner = relationship(
        "User",
        back_populates="documents",
    )

    conversation = relationship(
        "Conversation",
        back_populates="documents",
    )


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    is_pinned = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    pinned_at = Column(
        DateTime,
        nullable=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="conversations",
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )

    documents = relationship(
        "Document",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )


class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=False,
    )

    role = Column(
        String,
        nullable=False,
    )

    content = Column(
        String,
        nullable=False,
    )
    
    sources = Column(
        JSON,
        nullable=False,
        default=list,
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )  