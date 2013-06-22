""" Strategies to Traverse a Tree """
from strategies.core import chain, do_one
from term import new, op, args, isleaf

def top_down(rule):
    """ Apply a rule down a tree running it on the top nodes first """
    return chain(rule, lambda expr: sall(top_down(rule))(expr))

def bottom_up(rule):
    """ Apply a rule down a tree running it on the bottom nodes first """
    return chain(lambda expr: sall(bottom_up(rule))(expr), rule)

def top_down_once(rule):
    """ Apply a rule down a tree - stop on success """
    return do_one(rule, lambda expr: sall(top_down(rule))(expr))

def bottom_up_once(rule):
    """ Apply a rule up a tree - stop on success """
    return do_one(lambda expr: sall(bottom_up(rule))(expr), rule)

def sall(rule):
    """ Strategic all - apply rule to args """
    def all_rl(expr):
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
    return all_rl
