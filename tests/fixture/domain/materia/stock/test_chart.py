from fixture.domain.materia.stock.chart import factory_bar, factory_chart
from src.domain.materia.alpaca.bar.model import Bar, Chart


def test_factory_bar():
    bar = factory_bar()
    assert isinstance(bar, Bar)
    # 対象モックナンバーであることを確認
    assert bar.volume == 114514.305358


def test_factory_chart():
    chart = factory_chart()
    assert isinstance(chart, Chart)
    # 対象モックオブジェクトであることを確認
    assert chart.symbol == "MOCKSYMBOL_94CE5395"
