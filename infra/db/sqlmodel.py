from dataclasses import dataclass
from typing import List, Optional

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

    def select_models(
        self,
        model: type[SQLModel],
        conditions: Optional[dict] = None
    ) -> List[SQLModel]:
        """
        NOTE: stmtを直接渡すシンプルな形式に変える？

            modelとconditionsを別々に渡す形式である必要があまりない気がしてきた。
            なぜならconditionsを作る時点でmodelが密接に関連しているからだ。

            だったらstmtのリストを渡す形にして、それをそのままsession管理しつつ実行、
            という形のほうが機能として合理的ではないだろうか。
            今の実装であればこれをリポジトリから呼び出した場合、
            インフラ層のモデルをリポジトリが意識してしまう状態となるためマズい。

            stmtの作成は、infra/db/queryあたりに集めてそれを呼び出す形とすればいい。
            そうすればリポジトリ側からインフラ側の実装を秘匿できる上、
            気にするのはstmtの条件の数値だけで済む。

        懸念:
            今の所この関数はselectで使うという想定となっている。
            だがこの関数の機能が実行というところに注力して作られているならば、
            これがselectにしか使われないということはないのではないだろうか？

            > 1:
                ありそうなケースはdelete,updateしてからselectみたいなケース。
                着地地点はselectというルールでこれを設計するならば、
                戻り値はこのままのall()でいいのではないか。

                それにupdateやdeleteで終わってall()の結果が帰ったとしても、
                それを使わなければいいだけの話で動作に支障はない。
        """
        with self.session() as session:
            stmt = select(model)
            if conditions:
                stmt = stmt.filter_by(**conditions)
            return session.exec(stmt).all()