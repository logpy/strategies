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
            return      x
    return conditioned_rl

def chain(*fns):
    """
    Compose a sequence of fns so that they apply to the x sequentially
    """
    def chain_rl(x):
        for fn in fns:
            x = fn(x)
        return x
    return chain_rl

def debug(fn, file=None):
    """ Print out before and after xessions each time fn is used """
    if file is None:
        from sys import stdout
        file = stdout
    def debug_rl(x):
        result = fn(x)
        if result != x:
            file.write("fn:  %s\n"%fn.func_name)
            file.write("In:  %s\nOut: %s\n\n"%(x, result))
        return result
    return debug_rl

def null_safe(fn):
    """ Return original x if fn returns None """
    def null_safe_rl(x):
        result = fn(x)
        if result is None:
            return x
        else:
            return result
    return null_safe_rl

def tryit(fn):
    """ Return original x if fn raises exception """
    def try_rl(x):
        try:
            return fn(x)
        except:
            return x
    return try_rl

def do_one(*fns):
    """ Try each of the fns until one works. Then stop. """
    def do_one_rl(x):
        for rl in fns:
            result = rl(x)
            if result != x:
                return result
        return x
    return do_one_rl

def switch(key, fndict):
    """ Select a fn based on the result of key called on the function """
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
    """ Select result of fns that minimizes objective

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
