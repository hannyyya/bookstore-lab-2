from django.urls import path
from .views import *
urlpatterns = [
    path("", index),
    path("create/", create),
    path("login/", login),
    path("index/<int:id>/", addInCart),
    path("logout/", logout),
    path("cart/", cart),
    path("personalArea/", editUser),
    path("registration/", registration),
    path("order/", order),
    path("orderList/", orderList),
    path("edit/<int:id>/", edit),
    path("delete/<int:id>/", delete),
]