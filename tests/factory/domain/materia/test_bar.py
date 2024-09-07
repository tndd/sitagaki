from domain.materia.bar.model import Bar
from tests.utils.factory.domain.materia.bar import (generate_bar,
                                                    generate_bar_list)


def test_generate_bar():
    bar = generate_bar()
    assert isinstance(bar, Bar)


def test_generate_bar_list():
    bars = generate_bar_list()
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)