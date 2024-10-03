from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import Engine, Table, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.expression import Insert, Select

Base = declarative_base()

class SQLAlchemyClient:
    def __init__(self, engine: Engine):
        self.engine: Engine = engine
        self.Session: sessionmaker = sessionmaker(bind=engine)

    @contextmanager
    def session_scope(self):
        session: Session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    # ORM用メソッド
    def insert_models(self, models: list) -> None:
        with self.session_scope() as session:
            session.add_all(models)

    def query(self, model_class: type, *criterion: Any) -> List[Any]:
        with self.session_scope() as session:
            return session.query(model_class).filter(*criterion).all()

    # Core用メソッド
    def execute_core_query(self, query: Union[Select, str], params: Optional[Dict[str, Any]] = None) -> List[Any]:
        with self.engine.connect() as connection:
            if params:
                result = connection.execute(query, params)
            else:
                result = connection.execute(query)
            return result.fetchall()

    def insert_core(self, table: Table, values: List[Dict[str, Any]]) -> None:
        with self.engine.connect() as connection:
            connection.execute(table.insert(), values)

    # 汎用的なクエリ実行メソッド（文字列SQLにも対応）
    def execute_query(self, query: Union[str, Select, Insert], params: Optional[Dict[str, Any]] = None) -> List[Any]:
        with self.session_scope() as session:
            if isinstance(query, str):
                result = session.execute(text(query), params)
            else:
                result = session.execute(query, params)
            return result.fetchall()

    # テーブル作成メソッド
    def create_tables(self) -> None:
        Base.metadata.create_all(self.engine)

    def drop_tables(self) -> None:
        Base.metadata.drop_all(self.engine)
