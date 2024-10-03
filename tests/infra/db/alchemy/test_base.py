from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from infra.db.alchemy.client import SQLAlchemyModel


def test_to_params():
    class TestModel(SQLAlchemyModel):
        __tablename__ = "__test_table"
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String)
        email: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    test_model = TestModel(id=1, name="test")
    test_model_params = test_model.to_params()
    # Noneの要素が除外されていることを確認
    assert test_model_params == {"id": 1, "name": "test"}
