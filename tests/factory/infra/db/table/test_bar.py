from infra.db.table.bar import TblBarBase
from tests.utils.factory.infra.db.table.bar import (
    generate_tbl_bar_base,
    generate_tbl_bar_base_list,
)


def test_generate_tbl_bar_base():
    tbl_bar_base = generate_tbl_bar_base()
    assert isinstance(tbl_bar_base, TblBarBase)


def test_generate_tbl_bar_base_list():
    tbl_bar_base_list = generate_tbl_bar_base_list()
    assert isinstance(tbl_bar_base_list, list)
    assert all(isinstance(tbl_bar_base, TblBarBase) for tbl_bar_base in tbl_bar_base_list)
