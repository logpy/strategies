from .dispatch import dispatch


@dispatch((tuple, list))
def arguments(seq):
    return seq[1:]


@dispatch((tuple, list))
def operator(seq):
    return seq[0]


@dispatch(object, (tuple, list))
def term(op, args):
    return (op,) + tuple(args)
