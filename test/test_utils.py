from curtains.utils import pairwise


def test_pairwise():
    l = [0,4,7,9]
    iter = pairwise(l)
    assert next(iter) == (0, 4)
    assert next(iter) == (4, 7)
    assert next(iter) == (7, 9)