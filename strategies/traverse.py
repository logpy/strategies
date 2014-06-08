""" Strategies to Traverse a Tree """
from .core import chain, do_one
from logpy.term import operator, arguments, term
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
    try:
        op = operator(expr)
        children = arguments(expr)
        if children:
            children = list(map(rule, children))
        return term(op, children)
    except NotImplementedError:
        return expr
