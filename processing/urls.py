from django.urls import re_path
from processing.views import *


urlpatterns = [
    re_path(r"^upload/$", UploadView.as_view(), name="upload"),
    # re_path(r"^status/$", StatusView.as_view(), name="status"),
]
