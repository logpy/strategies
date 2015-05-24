""" Strategies to Traverse a Tree """
from .core import chain, do_one
from toolz import curry

@curry
def top_down(rule, x):
    """ Apply a rule down a tree running it on the top nodes first """
    return chain([rule, lambda expr: sall(top_down(rule))(expr)], x)

@curry
def bottom_up(rule, x):
    """ Apply a rule down a tree running it on the bottom nodes first """
    return chain([lambda expr: sall(bottom_up(rule))(expr), rule], x)

@curry
def top_down_once(rule, x):
    """ Apply a rule down a tree - stop on success """
    return do_one([rule, lambda expr: sall(top_down(rule))(expr)], x)

@curry
def bottom_up_once(rule, x):
    """ Apply a rule up a tree - stop on success """
    return do_one([lambda expr: sall(bottom_up(rule))(expr), rule], x)

@curry
def sall(rule, expr):
    """ Strategic all - apply rule to args """
    op, new, children, leaf = map(fns.get, ('op', 'new', 'children', 'leaf'))
    def all_rl(expr):
        if leaf(expr):
            return expr
        else:
            args = map(rule, children(expr))
            return new(op(expr), *args)
    return all_rl
