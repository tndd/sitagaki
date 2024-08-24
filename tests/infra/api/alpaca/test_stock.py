from infra.api.alpaca.stock import f


def test_f():
    bars = f()
    with open('out/output.txt', 'w') as file:
        file.write(str(bars))
    assert 1 + 1 == 2