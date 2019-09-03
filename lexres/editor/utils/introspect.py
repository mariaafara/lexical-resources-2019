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
