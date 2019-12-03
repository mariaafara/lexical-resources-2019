from django.shortcuts import render, redirect
from django.http import JsonResponse

# utilities for introspection
from .utils.introspect import as_dict

# specific modules
from .nlp.services import preds as preds_module
from .nlp.services import edits as edits_module

def editor(request):
    return render(request, "editor/editor.html")

def ajax_preds(request):
    return JsonResponse(as_dict(preds_module, request))

def ajax_edits(request):
    return JsonResponse(as_dict(edits_module, request, coerce=True))

def handle_404(request, exception):
    return redirect("editor")
