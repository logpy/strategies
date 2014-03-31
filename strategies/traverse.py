""" Strategies to Traverse a Tree """
from strategies.core import chain, do_one
from term import new, op, args, isleaf
from toolz import curry

@curry
def top_down(rule, x):
    """ Apply a rule down a tree running it on the top nodes first """
    return chain(rule, lambda expr: sall(top_down(rule))(expr))(x)

@curry
def bottom_up(rule, x):
    """ Apply a rule down a tree running it on the bottom nodes first """
    return chain(lambda expr: sall(bottom_up(rule))(expr), rule)(x)

@curry
def top_down_once(rule, x):
    """ Apply a rule down a tree - stop on success """
    return do_one(rule, lambda expr: sall(top_down(rule))(expr))(x)

@curry
def bottom_up_once(rule, x):
    """ Apply a rule up a tree - stop on success """
    return do_one(lambda expr: sall(bottom_up(rule))(expr), rule)(x)

@curry
def sall(rule, expr):
    """ Strategic all - apply rule to args """
    if isleaf(expr):
        return expr
    else:
        children = args(expr)
        if isinstance(children, (tuple, list)):
            children = map(rule, children)
        if isinstance(children, dict):
            children = dict(zip(children.keys(),
                            map(sall(rule), children.values())))
        return new(op(expr), children)
