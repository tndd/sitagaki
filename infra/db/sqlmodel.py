from dataclasses import dataclass
from typing import List

from sqlalchemy.engine.base import Engine
from sqlmodel import Session, SQLModel
from sqlmodel.sql.expression import SelectOfScalar


@dataclass
class SQLModelClient:
    engine: Engine

    def session(self) -> Session:
        return Session(self.engine)

    def insert_models(self, models: list[SQLModel]):
        """
        渡されたモデルそのままDBに登録する。
        """
        # TODO: 引数が１つのモデルである場合、自動的にリストに変換する
        with self.session() as session:
            session.add_all(models)
            session.commit()

    def select_models(self, stmt: SelectOfScalar) -> List[SQLModel]:
        """
        selectステートメントを実行し、モデルのリストを返す。
        """
        with self.session() as session:
            result = session.exec(stmt).all()
        return result