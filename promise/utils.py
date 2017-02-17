import functools
import inspect
import warnings


class deprecated(object):

    def __init__(self, reason, name=None):
        if inspect.isclass(reason) or inspect.isfunction(reason):
            raise TypeError("Reason for deprecation must be supplied")
        self.reason = reason
        self.name = name

    def __call__(self, cls_or_func):
        if inspect.isfunction(cls_or_func):
            fmt = "Call to deprecated function or method {name} ({reason})."

        elif inspect.isclass(cls_or_func):
            fmt = "Call to deprecated class {name} ({reason})."

        else:
            raise TypeError(type(cls_or_func))

        msg = fmt.format(name=self.name or cls_or_func.__name__, reason=self.reason)

        @functools.wraps(cls_or_func)
        def new_func(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)  # turn off filter
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)  # reset filter
            return cls_or_func(*args, **kwargs)

        return new_func