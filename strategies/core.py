""" Generic SymPy-Independent Strategies """
from functools import partial

identity = lambda x: x

def exhaust(fn):
    """ Apply a fn repeatedly until it has no effect """
    def exhaustive_rl(x):
        new, old = fn(x), x
        while(new != old):
            new, old = fn(new), new
        return new
    return exhaustive_rl

def memoize(fn):
    """ Memoized version of a fn """
    cache = {}
    def memoized_rl(x):
        if x in cache:
            return cache[x]
        else:
            result = fn(x)
            cache[x] = result
            return result
    return memoized_rl

def condition(cond, fn):
    """ Only apply fn if condition is true """
    def conditioned_rl(x):
        if cond(x):
            return fn(x)
        else:
            return x
    return conditioned_rl

def chain(*fns):
    """ Sequentially apply a sequence of functions """
    def chain_rl(x):
        for fn in fns:
            x = fn(x)
        return x
    return chain_rl

def onaction(fn, action):
    def onaction_brl(x):
        result = fn(x)
        if result != x:
            action(fn, x, result)
        return result
    return onaction_brl

def debug(fn, file=None):
    """ Print input and output each time function has an effect """
    if not file:
        from sys import stdout
        file = stdout

    def write(fn, x, result):
        file.write("Fn:  %s\n"%fn.func_name)
        file.write("In:  %s\nOut: %s\n\n"%(x, result))

    return onaction(fn, write)

def do_one(*fns):
    """ Try each of the functions until one works. Then stop. """
    def do_one_rl(x):
        for rl in fns:
            result = rl(x)
            if result != x:
                return result
        return x
    return do_one_rl

def switch(key, fndict):
    """ Select a function based on the result of key called on the function """
    def switch_rl(x):
        rl = fndict.get(key(x), identity)
        return rl(x)
    return switch_rl

def typed(fntypes):
    """ Apply fns based on the input type

    inputs:
        fntypes -- a dict mapping {Type: fn}

    >>> from strategies.examples import inc, dec
    >>> f = typed({int: inc, float: dec})
    >>> f(3)
    4
    >>> f(3.0)
    2.0
    """
    return switch(type, fntypes)

def minimize(*fns, **kwargs):
    """ Select result of functions that minimizes objective

    >>> from sympy.strategies import minimize
    >>> from strategies.examples import inc, dec
    >>> rl = minimize(inc, dec)
    >>> rl(4)
    3

    >>> rl = minimize(inc, dec, objective=lambda x: -x)  # maximize
    >>> rl(4)
    5
    """

    objective = kwargs.get('objective', identity)
    def minfn(x):
        return min([fn(x) for fn in fns], key=objective)
    return minfn
