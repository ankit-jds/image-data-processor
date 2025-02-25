import time
import logging

import os
import requests
from io import BytesIO
from PIL import Image
from django.conf import settings
from celery import shared_task
from processing.models import ImageProcessingRequest  ,  CSVRequest, ProductEntry

# Set up logger for your task
logger = logging.getLogger(__name__)

@shared_task
def long_running_task(unique_id):
    """
    Simulate a long-running background task.
    """
    # print(f"Starting background job with ID: {unique_id}")
    # time.sleep(10)  # Simulating a long task (10 seconds)
    # print(f"Background job with ID: {unique_id} is complete.")

    logger.info(f"Starting background job with ID: {unique_id}")
    time.sleep(10)  # Simulating a long task (10 seconds)
    logger.info(f"Background job with ID: {unique_id} is complete.")


@shared_task
def process_images_old(request_id):
    request_obj = ImageProcessingRequest.objects.get(request_id=request_id)
    request_obj.status = 'processing'
    request_obj.save()

    input_urls = request_obj.input_urls.split(',')
    output_urls = []

    # Ensure MEDIA_ROOT exists
    media_root = settings.MEDIA_ROOT
    os.makedirs(media_root, exist_ok=True)


    for url in input_urls:
        if "http" not in url:
            output_urls.append(url)
            continue

        response = requests.get(url.strip())
        img = Image.open(BytesIO(response.content))

        # Compress image (50% quality)
        output_buffer = BytesIO()
        img.save(output_buffer, format="JPEG", quality=50)
        output_buffer.seek(0)

        # Upload to ImgBB
        imgbb_api_key = settings.IMGBB_API_KEY
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": imgbb_api_key},
            files={"image": output_buffer}
        )
        print(response)
        print(response.json())
        output_urls.append(response.json()["data"]["url"])

    request_obj.output_urls = ','.join(output_urls)
    request_obj.status = 'completed'
    request_obj.save()
    # Trigger webhook (optional)
    # requests.post('user_webhook_url', json={"request_id": str(request_id), "output_urls": output_urls})

@shared_task
def process_images(request_id):
    csv_request = CSVRequest.objects.get(request_id=request_id)
    csv_request.status = 'processing'
    csv_request.save()

    # Process all entries for this request
    entries = ProductEntry.objects.filter(request=csv_request)
    for entry in entries:
        input_urls = entry.input_urls.split(',')
        output_urls = []

        for idx, url in enumerate(input_urls):
            print(url,"start")
            if "http" not in url:
                output_urls.append(url)
                continue
            response = requests.get(url.strip())
            img = Image.open(BytesIO(response.content))
            output_buffer = BytesIO()
            img.save(output_buffer, format="JPEG", quality=50)

            output_buffer.seek(0)

            # Upload to ImgBB
            imgbb_api_key = settings.IMGBB_API_KEY
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                data={"key": imgbb_api_key},
                files={"image": output_buffer}
            )
            print(response)
            print(response.json())
            output_urls.append(response.json()["data"]["url"])
            
        entry.output_urls = ','.join(output_urls)
        entry.save()

    # Update request status
    csv_request.status = 'completed'
    csv_request.save()

    # Trigger webhook if provided
    if csv_request.webhook_url:
        webhook_payload = [
            {
                "Serial Number": entry.serial_no,
                "Product Name": entry.product_name,
                "Input Image Urls": entry.input_urls,
                "Output Image Urls": entry.output_urls
            } for entry in entries
        ]
        try:
            requests.post(csv_request.webhook_url, json=webhook_payload, timeout=5)
        except requests.RequestException as e:
            # Log the error (in production); for now, ignore silently
            pass