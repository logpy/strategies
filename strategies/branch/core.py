""" Generic SymPy-Independent Strategies """
from toolz import curry, filter

def identity(x):
    yield x

@curry
def exhaust(fn, x):
    """ Apply a branching rule repeatedly until it has no effect """
    seen = set([x])
    for nx in fn(x):
        if nx not in seen:
            seen.add(nx)
            for nnx in exhaust(fn, nx):
                yield nnx
    if seen == set([x]):
        yield x

@curry
def onaction(fn, action, x):
    for result in fn(x):
        if result != x:
            action(fn, x, result)
        yield result

def debug(fn, file=None):
    """ Print the input and output expressions at each rule application """
    if not file:
        from sys import stdout
        file = stdout

    def write(brl, x, result):
        file.write("Rule: %s\n"%brl.__name__)
        file.write("In: %s\nOut: %s\n\n"%(x, result))

    return onaction(fn, write)

@curry
def multiplex(fns, x):
    """ Multiplex many branching rules into one """
    seen = set([])
    for brl in fns:
        for nx in brl(x):
            if nx not in seen:
                seen.add(nx)
                yield nx

@curry
def condition(cond, fn, x):
    """ Only apply branching rule if condition is true """
    if cond(x):
        for x in fn(x):
            yield x
    else:
        pass

@curry
def sfilter(pred, fn, x):
    """ Yield only those results which satisfy the predicate """
    for x in filter(pred, fn(x)):
        yield x

@curry
def notempty(fn, x):
    yielded = False
    for nx in fn(x):
        yielded = True
        yield nx
    if not yielded:
        yield x

@curry
def do_one(fns, x):
    """ Execute one of the branching rules """
    yielded = False
    for brl in fns:
        for nx in brl(x):
            yielded = True
            yield nx
        if yielded:
            raise StopIteration()

@curry
def chain(fns, x):
    """
    Compose a sequence of fns so that they apply to the expr sequentially
    """
    if not fns:
        yield x
        raise StopIteration()

    head, tail = fns[0], fns[1:]
    for nx in head(x):
        for nnx in chain(tail)(nx):
            yield nnx


@curry
def yieldify(rl, x):
    """ Turn a rule into a branching rule """
    yield rl(x)
