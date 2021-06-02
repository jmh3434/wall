from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('login',views.login),
    path('register',views.register),
    path('success',views.success),
    path('logout',views.logout),
    path('create_post',views.create_post),
    path('add_comment/<int:id>',views.add_comment),
    path('like/<int:id>',views.like),
]