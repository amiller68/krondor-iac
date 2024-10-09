from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid
from sqlalchemy.future import select

import sys

sys.path.append("..")

# Import our Base class
from app.logger import RequestSpan
from .database import Base, DatabaseException


class Example(Base):
    __tablename__ = "examples"

    # Unique identifier
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)

    # email
    example = Column(String, unique=True, nullable=False)

    # timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    def dict(self):
         return {
            "id": self.id,
            "example": self.example,
            "created_at": self.created_at.isoformat(),
        }

    @staticmethod
    async def create(
        example: str, session: AsyncSession, span: RequestSpan | None = None
    ):
        try:
            example = Example(example=example)
            session.add(example)
            await session.flush()
            return user
        except Exception as e:
            if span:
                span.error(f"database::models::Example::create: {e}")
            db_e = DatabaseException.from_sqlalchemy_error(e)
            raise db_e

    @staticmethod
    async def read(id: str, session: AsyncSession, span: RequestSpan | None = None):
        try:
            result = await session.execute(select(Example).filter_by(id=id))
            return result.scalars().first()
        except Exception as e:
            if span:
                span.error(f"database::models::User::read: {e}")
            db_e = DatabaseException.from_sqlalchemy_error(e)
            raise db_e