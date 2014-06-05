""" Generic SymPy-Independent Strategies """
from toolz import curry, memoize, identity


@curry
def exhaust(fn, x):
    """ Apply a fn repeatedly until it has no effect """
    new, old = fn(x), x
    while(new != old):
        new, old = fn(new), new
    return new


@curry
def condition(cond, fn, x):
    """ Only apply fn if condition is true """
    if cond(x):
        return fn(x)
    else:
        return x


@curry
def chain(fns, x):
    """ Sequentially apply a sequence of functions """
    for fn in fns:
        x = fn(x)
    return x


@curry
def onaction(fn, action, x):
    result = fn(x)
    if result != x:
        action(fn, x, result)
    return result


def debug(fn, file=None):
    """ Print input and output each time function has an effect """
    if not file:
        from sys import stdout
        file = stdout

    def write(fn, x, result):
        file.write("Fn:  %s\n"%fn.__name__)
        file.write("In:  %s\nOut: %s\n\n"%(x, result))

    return onaction(fn, write)


@curry
def do_one(fns, x):
    """ Try each of the functions until one works. Then stop. """
    for fn in fns:
        result = fn(x)
        if result != x:
            return result
    return x


@curry
def switch(key, fndict, x):
    """ Select a function based on the result of key called on the function """
    fn = fndict.get(key(x), identity)
    return fn(x)


@curry
def typed(fntypes, x):
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
    return switch(type, fntypes, x)


@curry
def minimize(fns, x, **kwargs):
    """ Select result of functions that minimizes objective

    >>> from strategies import minimize
    >>> from strategies.examples import inc, dec
    >>> fn = minimize([inc, dec])
    >>> fn(4)
    3

    >>> fn = minimize([inc, dec], objective=lambda x: -x)  # maximize
    >>> fn(4)
    5
    """
    objective = kwargs.get('objective', identity)
    return min([fn(x) for fn in fns], key=objective)
