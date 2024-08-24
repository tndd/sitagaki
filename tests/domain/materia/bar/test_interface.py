from domain.materia.bar.interface import update_bars


# pytestの動作を確認するための簡易テストを実装
def test_test_interface():
    update_bars()
    assert 1 + 1 == 2
