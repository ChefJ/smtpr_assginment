from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Contact, Label


def api_test_page(request):
    return render(request, "contactbook/test_api.html")


def delete_object(request, model, obj_name="object"):
    obj_id = request.GET.get("id")
    if not obj_id:
        return HttpResponseBadRequest("id is required")

    try:
        obj = model.objects.get(id=obj_id)
    except model.DoesNotExist:
        return HttpResponseBadRequest(f"{obj_name} not found")

    obj.delete()
    return JsonResponse({"status": "ok", "deleted_id": obj_id})


def parse_body(request):
    try:
        return json.loads(request.body.decode()) if request.body else {}
    except json.JSONDecodeError:
        return {}


@require_http_methods(["POST"])
def contact_create(request):
    data = parse_body(request)
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    if not name or not email or not phone:
        return HttpResponseBadRequest("name, phone and email are required")

    contact = Contact.objects.create(name=name, email=email, phone=phone)
    return JsonResponse({"id": contact.id, "name": contact.name, "email": contact.email, "phone": contact.phone})


@require_http_methods(["POST"])
def contact_list(request):
    qs = Contact.objects.all()

    labels_param = request.GET.get("labels", "")
    if labels_param:
        label_names = [n.strip() for n in labels_param.split(",") if n.strip()]
        if not label_names:
            return HttpResponseBadRequest("no valid label names")
        qs = qs.filter(labels__name__in=label_names).distinct()

    emails_only = request.GET.get("emails_only", "").lower() in ("1", "true", "yes")

    if emails_only:
        emails = (
            qs.exclude(email="")
            .values_list("email", flat=True)
            .distinct()
        )
        return JsonResponse({"emails": list(emails)})

    contacts = []
    for a_contact in qs.prefetch_related("labels"):
        contacts.append({
            "id": a_contact.id,
            "name": a_contact.name,
            "email": a_contact.email,
            "phone": a_contact.phone,
            "labels": [a_label.name for a_label in a_contact.labels.all()],
        })

    return JsonResponse(contacts, safe=False)


@require_http_methods(["GET"])
def contact_del(request):
    return delete_object(request, Contact, "contact")


@require_http_methods(["POST"])
def label_create(request):
    data = parse_body(request)
    name = data.get("name")
    if not name:
        return HttpResponseBadRequest("name is required")

    label, created = Label.objects.get_or_create(name=name)
    return JsonResponse({"id": label.id, "name": label.name, "created": created})


@require_http_methods(["GET"])
def label_list(request):
    labels = Label.objects.all().values("id", "name")
    return JsonResponse(list(labels), safe=False)


@require_http_methods(["GET"])
def label_del(request):
    return delete_object(request, Label, "label")


def true_del(request):
    return HttpResponse("OK")


@require_http_methods(["POST"])
def add_label(request):
    data = parse_body(request)
    contact_id = data.get("contact_id")
    label_names = data.get("labels", [])  # 这里用 label 名，会比较直观

    if not contact_id or not label_names:
        return HttpResponseBadRequest("contact_id and labels are required")

    try:
        contact = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist:
        return HttpResponseBadRequest("contact not found")

    labels = []
    for name in label_names:
        lbl, _ = Label.objects.get_or_create(name=name)
        labels.append(lbl)

    contact.labels.add(*labels)

    return JsonResponse({
        "contact_id": contact.id,
        "labels": [l.name for l in contact.labels.all()]
    })


@require_http_methods(["POST"])
def remove_label(request):
    data = parse_body(request)

    contact_id = data.get("contact_id")
    label_names = data.get("labels", [])

    if not contact_id or not label_names:
        return HttpResponseBadRequest("contact_id and labels are required")

    try:
        contact = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist:
        return HttpResponseBadRequest("contact not found")

    labels = Label.objects.filter(name__in=label_names)
    contact.labels.remove(*labels)

    return JsonResponse({
        "contact_id": contact.id,
        "labels": [l.name for l in contact.labels.all()]
    })
