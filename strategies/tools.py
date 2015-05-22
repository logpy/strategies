from __future__ import print_function, division

from .core import do_one, exhaust, switch


def typed(ruletypes):
    """Apply rules based on the expression type

    inputs:
        ruletypes -- a dict mapping {Type: rule}
    """
    return switch(type, ruletypes)
