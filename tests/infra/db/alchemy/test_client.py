from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from infra.db.alchemy.client import SQLAlchemyModel


class TestModel(SQLAlchemyModel):
    __tablename__ = "__test_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)


def test_insert_models(test_alchemy_cli):
    """
    ３件のデータを投入し、その内容を確認する。
    """
    models = [
        TestModel(id=1, name='user1', email='user1@example.com'),
        TestModel(id=2, name='user2', email='user2@example.com'),
        TestModel(id=3, name='user3', email='user3@example.com')
    ]
    test_alchemy_cli.insert_models(models)
    result = test_alchemy_cli.select_models(TestModel)
    assert len(result) == 3
    assert result[0].name == 'user1'
    assert result[1].name == 'user2'
    assert result[2].name == 'user3'
