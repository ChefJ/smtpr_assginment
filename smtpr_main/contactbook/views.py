from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Contact, Label


def api_test_page(request):
    return HttpResponse("ok")


def parse_body(request):
    try:
        return json.loads(request.body.decode()) if request.body else {}
    except json.JSONDecodeError:
        return {}


def contact_create(request):
    return HttpResponse("ok")


def contact_list(request):
    return HttpResponse("ok")


def contact_del(request):
    return HttpResponse("ok")


def label_create(request):
    return HttpResponse("ok")


def label_list(request):
    return HttpResponse("ok")


def label_del(request):
    return HttpResponse("ok")


def true_del(request):
    return HttpResponse("OK")


def add_label(request):
    return HttpResponse("OK")


def remove_label(request):
    return HttpResponse("OK")
