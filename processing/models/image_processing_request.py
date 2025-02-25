from django.db import models
import uuid

class ImageProcessingRequest(models.Model):
    request_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    serial_no = models.IntegerField()
    product_name = models.CharField(max_length=255)
    input_urls = models.TextField()  
    output_urls = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request_id} - {self.product_name}"