from django.db import models
import uuid
from processing.models import CSVRequest

class ProductEntry(models.Model):
    request = models.ForeignKey(CSVRequest, on_delete=models.CASCADE, related_name='entries')
    serial_no = models.IntegerField()
    product_name = models.CharField(max_length=255)
    input_urls = models.TextField()
    output_urls = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.product_name} (Request {self.request.request_id})"