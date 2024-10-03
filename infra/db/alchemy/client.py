from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import Engine, Table, select, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.sql import Select


class SQLAlchemyModel(DeclarativeBase):
    def to_params(self):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if getattr(self, c.name) is not None
        }


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
    def insert_models(self, models: List[DeclarativeBase]) -> None:
        with self.session_scope() as session:
            session.bulk_save_objects(models)

    def select_models(self, model_class: type, *criterion: Any) -> List[Any]:
        with self.session_scope() as session:
            stmt = select(model_class).filter(*criterion)
            result = session.execute(stmt)
            return result.scalars().all()

    # Core用メソッド
    def core_insert_models(self, models: List[DeclarativeBase]) -> None:
        with self.session_scope() as session:
            session.execute


    def execute_core_query(self, query: Union[Select, str], params: Optional[Dict[str, Any]] = None) -> List[Any]:
        with self.engine.connect() as connection:
            if isinstance(query, str):
                query = text(query)
            result = connection.execute(query, params)
            return result.fetchall()

    def insert_core(self, table: Table, values: List[Dict[str, Any]]) -> None:
        with self.engine.connect() as connection:
            connection.execute(table.insert(), values)
            connection.commit()

    # 汎用的なクエリ実行メソッド
    def execute_query(self, query: Union[str, Select], params: Optional[Dict[str, Any]] = None) -> List[Any]:
        with self.session_scope() as session:
            if isinstance(query, str):
                query = text(query)
            result = session.execute(query, params)
            return result.fetchall()