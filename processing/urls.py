from django.urls import re_path
from processing.views import *
from .utils import start_scheduler

start_scheduler()

urlpatterns = [
    re_path(r"^upload/$", UploadView.as_view(), name="upload"),
    # re_path(r"^status/$", StatusView.as_view(), name="status"),
]
