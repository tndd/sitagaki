from domain.materia.bar.model import Bar, Chart
from tests.utils.factory.domain.materia.bar import generate_bar, generate_chart


def test_generate_bar():
    bar = generate_bar()
    assert isinstance(bar, Bar)


def test_generate_chart():
    chart = generate_chart()
    assert isinstance(chart, Chart)
