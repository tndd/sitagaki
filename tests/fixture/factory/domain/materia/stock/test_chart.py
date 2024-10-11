from fixture.factory.domain.materia.stock.chart import generate_bar, generate_chart
from src.domain.materia.stock.chart.model import Bar, Chart


def test_generate_bar():
    bar = generate_bar()
    assert isinstance(bar, Bar)
    # 対象モックナンバーであることを確認
    assert bar.volume == 114514.305358


def test_generate_chart():
    chart = generate_chart()
    assert isinstance(chart, Chart)
    # 対象モックオブジェクトであることを確認
    assert chart.symbol == "MOCKSYMBOL_94CE5395"
