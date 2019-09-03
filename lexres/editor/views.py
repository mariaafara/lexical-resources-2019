from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

# utilities for introspection
from .utils.introspect import as_dict

# specific modules
from .nlp.services import preds as preds_module
from .nlp.services import edits as edits_module

def editor(request):
    context = {"text":"DEFAULT", "predictions":[]}
    return render(request, "editor/editor.html", context)

def ajax_preds(request):
    return JsonResponse(as_dict(preds_module, request))

def ajax_edits(request):
    return JsonResponse(as_dict(edits_module, request, coerce=True))
