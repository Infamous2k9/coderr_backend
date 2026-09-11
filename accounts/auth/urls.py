from django.urls import path

from .views import RegistrationView

urlpatterns = [path("regisstration/", RegistrationView.as_view(), name="register")]
