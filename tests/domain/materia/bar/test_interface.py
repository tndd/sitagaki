from domain.materia.bar.interface import update_bars


# NOTE: これはpytestの動作を確認するための簡易テストでしかない
def test_test_interface():
    update_bars()
    assert 1 + 1 == 2
