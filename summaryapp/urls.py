from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.summary, name = "summarytop"),
    path("result/", views.result, name = "summaryresult"),
    path("contact/", views.contact, name = "summarycontact"),
]
