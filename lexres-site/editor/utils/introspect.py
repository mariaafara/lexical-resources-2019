from inspect import getmembers, isfunction

"""
    Utility functions for code introspection
"""

def list_funcs_in_module(module):
    """
        Retrieve functions from module
    """
    return [
        f for f,m in getmembers(module, isfunction)
        if m.__module__ == module.__name__
    ]

def run_func(module, func, *args, **kwargs):
    """
        Call specific function in module
    """
    return getattr(module, func)(*args, **kwargs)

def as_dict(module, request, coerce=False):
    """
        Create a JSON-compatible dict from module introspection & request
    """
    raw_data = request.GET.get("text", None)
    if not coerce:
        base = {
            f: run_func(module, f, text=raw_data)
            for f in list_funcs_in_module(module)
        }
    else:
        base = {
            f: list(map(list, run_func(module, f, text=raw_data)))
            for f in list_funcs_in_module(module)
        }
    base["orig_data"] = raw_data
    return base
