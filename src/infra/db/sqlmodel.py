from dataclasses import dataclass

from sqlalchemy.engine.base import Engine
from sqlmodel import Session, SQLModel, select


@dataclass
class SqlModelClient:
    engine: Engine

    def session(self) -> Session:
        return Session(self.engine)

    def insert_models(self, models: list[SQLModel]):
        with self.session() as session:
            session.add_all(models)
            session.commit()

    def select_models(self, model_class: type[SQLModel], conditions: dict) -> list[SQLModel]:
        with self.session() as session:
            stmt = select(model_class).filter_by(**conditions)
            return session.exec(stmt).all()