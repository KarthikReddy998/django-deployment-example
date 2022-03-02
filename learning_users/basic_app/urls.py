from . import views
from django.urls import path

#create name space

app_name="basic_app"

urlpatterns=[
    path('register/',views.register, name="register"),
    path('user_login/',views.user_login,name="user_login")
]