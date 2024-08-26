from dataclasses import dataclass

from pydantic import BaseModel
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, select


@dataclass
class SqlModelClient:
    engine: Engine

    def insert_models(self, models: list[SQLModel]):
        with Session(self.engine) as session:
            session.add_all(models)
            session.commit()

    def select_models(self, conditions: dict) -> list[SQLModel]:
        with Session(self.engine) as session:
            stmt = select(SQLModel).filter_by(**conditions)
            return session.exec(stmt).all()