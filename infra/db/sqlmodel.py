from dataclasses import dataclass
from typing import List

from sqlalchemy.engine.base import Engine
from sqlmodel import Session, SQLModel


@dataclass
class SqlModelClient:
    engine: Engine

    def session(self) -> Session:
        return Session(self.engine)

    def insert_models(self, models: list[SQLModel]):
        with self.session() as session:
            session.add_all(models)
            session.commit()


    def select_models(self, stmt: SQLModel) -> List[SQLModel]:
        """
        selectステートメントを実行し、モデルのリストを返す。
        """
        with self.session() as session:
            result = session.exec(stmt).all()
        return result