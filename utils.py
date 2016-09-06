#coding=utf-8

def arg(*args, **kwargs):
    """Decorator for CLI args.

    Example:

    >>> @arg("name", help="Name of the new entity")
    ... def entity_create(args):
    ...     pass
    """
    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func
    return _decorator
def add_arg(func, *args, **kwargs):
    """ Bind CLI arguments to a shell.py `do_foo` function."""
    if not hasattr(func, 'arguments'):
        func.arguments = []
    if (args, kwargs) not in func.arguments:
        func.arguments.insert(0, (args, kwargs))
