from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# utilities for introspection
from .utils.introspect import list_funcs_in_module, run_func

# specific modules
from .nlp.services import preds as preds_module
from .nlp.services import edits as edits_module

def index(request):
    return HttpResponse("Place holder for editor view")


def ajax_preds(request):
    for f in list_funcs_in_module(preds_module):
        run_func(preds_module, f)
    pass

def ajax_edits(request):
    for f in list_funcs_in_module(edits_module):
        run_func(preds_module, f)
    pass
