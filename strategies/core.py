""" Generic SymPy-Independent Strategies """
from functools import partial

identity = lambda x: x

def exhaust(fn):
    """ Apply a fn repeatedly until it has no effect """
    def exhaustive_fn(x):
        new, old = fn(x), x
        while(new != old):
            new, old = fn(new), new
        return new
    return exhaustive_fn

def memoize(fn):
    """ Memoized version of a fn """
    cache = {}
    def memoized_fn(x):
        if x in cache:
            return cache[x]
        else:
            result = fn(x)
            cache[x] = result
            return result
    return memoized_fn

def condition(cond, fn):
    """ Only apply fn if condition is true """
    def conditioned_fn(x):
        if cond(x):
            return fn(x)
        else:
            return x
    return conditioned_fn

def chain(*fns):
    """ Sequentially apply a sequence of functions """
    def chain_fn(x):
        for fn in fns:
            x = fn(x)
        return x
    return chain_fn

def onaction(fn, action):
    def onaction_fn(x):
        result = fn(x)
        if result != x:
            action(fn, x, result)
        return result
    return onaction_fn

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
    def do_one_fn(x):
        for fn in fns:
            result = fn(x)
            if result != x:
                return result
        return x
    return do_one_fn

def switch(key, fndict):
    """ Select a function based on the result of key called on the function """
    def switch_fn(x):
        fn = fndict.get(key(x), identity)
        return fn(x)
    return switch_fn

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
    >>> fn = minimize(inc, dec)
    >>> fn(4)
    3

    >>> fn = minimize(inc, dec, objective=lambda x: -x)  # maximize
    >>> fn(4)
    5
    """

    objective = kwargs.get('objective', identity)
    def minfn(x):
        return min([fn(x) for fn in fns], key=objective)
    return minfn
