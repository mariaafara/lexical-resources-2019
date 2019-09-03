"""
    Utility functions for code introspection
"""

def list_funcs_in_module(module):
    """
        Retrieve functions from module
    """
    return [f for f in dir(module) if f[0] != '_']

def run_func(module, func, *args, **kwargs):
    """
        Call specific function in module
    """
    return getattr(module, func)(*args, **kwargs)

def as_dict(module, request):
    """
        Create a JSON-compatible dict from module introspection & request
    """
    raw_data = request.GET.get("text", None)
    return {
        f: run_func(module, f, text=raw_data)
        for f in list_funcs_in_module(module)
    }
