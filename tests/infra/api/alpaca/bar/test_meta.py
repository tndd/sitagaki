import tests.infra.api.alpaca.bar.test_get_barset_alpaca_api as t
from tests.infra.api.alpaca.bar.test_get_barset_alpaca_api import h, h_direct


def test_h(monkeypatch):
    assert 'original' == h()
    monkeypatch.setattr(
        'infra.api.alpaca.bar.f',
        lambda: 'mocked'
    )
    assert 'mocked' == h()


def test_h_direct(monkeypatch):
    assert 'original' == h_direct()
    monkeypatch.setattr(
        'infra.api.alpaca.bar.f',
        lambda: 'mocked'
    )
    assert 'mocked' == h_direct()


def test_t_h(monkeypatch):
    """
    一度fromで呼んだモック化関数をimportしていると、
    それ以降はimport呼びしてもモック化されない
    """
    assert 'original' == t.h()
    monkeypatch.setattr(
        'infra.api.alpaca.bar.f',
        lambda: 'mocked'
    )
    assert 'mocked' == t.h()

