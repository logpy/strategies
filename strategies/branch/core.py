""" Generic SymPy-Independent Strategies """
import itertools

def identity(x):
    yield x

def exhaust(fn):
    """ Apply a branching rule repeatedly until it has no effect """
    def exhaust_brl(x):
        seen = set([x])
        for nx in fn(x):
            if nx not in seen:
                seen.add(nx)
                for nnx in exhaust_brl(nx):
                    yield nnx
        if seen == set([x]):
            yield x
    return exhaust_brl

def onaction(fn, action):
    def onaction_brl(x):
        for result in fn(x):
            if result != x:
                action(fn, x, result)
            yield result
    return onaction_brl

def debug(fn, file=None):
    """ Print the input and output expressions at each rule application """
    if not file:
        from sys import stdout
        file = stdout

    def write(brl, x, result):
        file.write("Rule: %s\n"%brl.func_name)
        file.write("In: %s\nOut: %s\n\n"%(x, result))

    return onaction(fn, write)

def multiplex(*fns):
    """ Multiplex many branching rules into one """
    def multiplex_brl(x):
        seen = set([])
        for brl in fns:
            for nx in brl(x):
                if nx not in seen:
                    seen.add(nx)
                    yield nx
    return multiplex_brl

def condition(cond, fn):
    """ Only apply branching rule if condition is true """
    def conditioned_brl(x):
        if cond(x):
            for x in fn(x): yield x
        else:
            pass
    return conditioned_brl

def sfilter(pred, fn):
    """ Yield only those results which satisfy the predicate """
    def filtered_brl(x):
        for x in itertools.ifilter(pred, fn(x)):
            yield x
    return filtered_brl

def notempty(fn):
    def notempty_brl(x):
        yielded = False
        for nx in fn(x):
            yielded = True
            yield nx
        if not yielded:
            yield x
    return notempty_brl

def do_one(*fns):
    """ Execute one of the branching rules """
    def do_one_brl(x):
        yielded = False
        for brl in fns:
            for nx in brl(x):
                yielded = True
                yield nx
            if yielded:
                raise StopIteration()
    return do_one_brl

def chain(*fns):
    """
    Compose a sequence of fns so that they apply to the expr sequentially
    """
    def chain_brl(x):
        if not fns:
            yield x
            raise StopIteration()

        head, tail = fns[0], fns[1:]
        for nx in head(x):
            for nnx in chain(*tail)(nx):
                yield nnx

    return chain_brl

def yieldify(rl):
    """ Turn a rule into a branching rule """
    def brl(x):
        yield rl(x)
    return brl
