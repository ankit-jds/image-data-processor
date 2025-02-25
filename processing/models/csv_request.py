from django.db import models
import uuid

class CSVRequest(models.Model):
    request_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    webhook_url = models.TextField(null=True, blank=True)  # Added for webhook

    def __str__(self):
        return f"Request {self.request_id}"
