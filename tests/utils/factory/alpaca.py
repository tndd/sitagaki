from alpaca.data.models import Bar, BarSet

from tests.utils.mock.loader import load


def make_barset_from_dict(data: dict) -> BarSet:
    bar_dicts = next(iter(data['data'].values()))
    # TODO: BarSetを作成
    return bar_dicts


def generate_barset() -> BarSet:
    data = load('barset.json')
    return make_barset_from_dict(data)
