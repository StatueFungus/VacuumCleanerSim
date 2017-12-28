from operator import is_not
from functools import partial


def filter_none(lis):
    return filter(partial(is_not, None), lis)