from domain.materia.stock.chart.model import Bar, Chart
from tests.utils.mock.domain.materia.stock.chart import generate_bar, generate_chart


def test_generate_bar():
    bar = generate_bar()
    assert isinstance(bar, Bar)


def test_generate_chart():
    chart = generate_chart()
    assert isinstance(chart, Chart)
