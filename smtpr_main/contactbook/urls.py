from django.urls import path

from . import views

urlpatterns = [
    path("contact/list", views.contact_list, name="contact_list"),
    path("contact/create", views.contact_create, name="contact_create"),
    path("contact/del/", views.contact_del, name="contact_del"),

    path("label/list", views.label_list, name="label_list"),
    path("label/create", views.label_create, name="label_create"),
    path("label/del", views.label_del, name="label_del"),

    path("contact/add_label", views.add_label, name="add_label"),
    path("contact/remove_label", views.remove_label, name="remove_label"),

    path("true_del", views.true_del, name="true_del"),
]