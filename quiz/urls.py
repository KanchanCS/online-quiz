from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "quiz"
urlpatterns = [
    path("", views.home, name="quiz"),
    path("register/", views.register, name="register"),
    path("login/", views.login_req, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("addQuestion/", views.addQuestion, name="addQuestion"),
]
