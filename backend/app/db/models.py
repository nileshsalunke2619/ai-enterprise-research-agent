from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    reports: Mapped[list["ResearchReport"]] = relationship(
        back_populates="user"
    )


class ResearchReport(Base):
    __tablename__ = "research_reports"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    report_content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="reports"
    )

    sources: Mapped[list["Source"]] = relationship(
        back_populates="report"
    )


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    title: Mapped[str | None] = mapped_column(
        String(500)
    )

    report_id: Mapped[int] = mapped_column(
        ForeignKey("research_reports.id"),
        nullable=False
    )

    report: Mapped["ResearchReport"] = relationship(
        back_populates="sources"
    )


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )