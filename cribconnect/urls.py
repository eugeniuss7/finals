from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("module2/", views.module2, name="module"),
    path("listingpage/<int:pk>", views.listingpage, name="listingpage"),
    path("propertylisting/", views.propertylisting, name="propertylisting"),
    path("createaccount/", views.createaccount, name="createaccount"),
    path("guest/",  views.guest_view, name="guest"),
    path("createaccount/account_form", views.account_form, name="accountform"),
    path("logout", views.logout_view, name="logout"),
    path("cribshare", views.cribshare_view, name="cribshare")
]