from django.urls import path
from processing.views import *
from .utils import start_scheduler


urlpatterns = [
    path("upload/", UploadView.as_view(), name="upload"),
    path("status/", StatusView.as_view(), name="status_list"),
    path("status/<str:request_id>/", StatusView.as_view(), name="status"),
]
