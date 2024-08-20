from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, SQLEnum, ForeignKey
from datetime import datetime
from enum import Enum

db = SQLAlchemy()


class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    tasks = db.relationship("Task", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="Untitled Task")
    description = db.Column(db.Text, nullable=False)
    status = db.Column(SQLEnum(Status), nullable=False, default=Status.PENDING)
    priority = db.Column(SQLEnum(Priority), nullable=False, default=Priority.LOW)
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)

    # relationship with user
    user = relationship("User", backref="tasks")

    def __repr__(self):
        return f"<Task {self.name} - Status: {self.status}>"
