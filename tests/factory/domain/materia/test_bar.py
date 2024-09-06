from domain.materia.bar.model import Bar
from tests.utils.factory.domain.materia.bar import generate_bar


def test_generate_bar():
    bar = generate_bar()
    assert isinstance(bar, Bar)