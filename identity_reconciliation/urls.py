from django.urls import path
from .views import IdentifyContact

urlpatterns = [
    path("identify/", IdentifyContact.as_view(), name="identify"),
]
