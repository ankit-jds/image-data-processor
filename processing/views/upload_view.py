from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from io import StringIO
import csv
import uuid
from processing.tasks import long_running_task, process_images
from processing.models import ImageProcessingRequest, CSVRequest, ProductEntry

class UploadView(APIView):
    def get(self, request):
        return Response(data={"message": "456454"}, status=status.HTTP_200_OK)

    # def post2(self, request):
    #     try:
    #         if "file" in request.FILES:
    #             file = request.FILES["file"]

    #         # Read the uploaded CSV file
    #         # csv_data = csv.reader(file.read().decode("utf-8").splitlines())

    #         # Process CSV data
    #         # rows = []
    #         # for row in csv_data:
    #         #     rows.append(row)  # You can process or save the row data here

    #         # Generate a unique ID for the background task
    #         unique_id = str(uuid.uuid4())

    #         # Trigger the Celery task asynchronously
    #         long_running_task.delay(unique_id)
    #         print("Res.")
    #         return Response(
    #             data={"uuid": unique_id}, status=status.HTTP_200_OK
    #         )

    #     except:
    #         import traceback

    #         print(traceback.format_exc())
    #         return Response(
    #             data={"error": "error hai"}, status=status.HTTP_400_BAD_REQUEST
    #         )

    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        webhook_url = request.data.get('webhook_url', "")
        if not csv_file:
            return Response({"error": "No CSV file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate CSV
        try:
            csv_text = csv_file.read().decode('utf-8')
            csv_reader = csv.reader(StringIO(csv_text))
            header = next(csv_reader)  # Check header
            if header != ['Serial Number', 'Product Name', 'Input Image Urls']:
                return Response({"error": "Invalid CSV format"}, status=status.HTTP_400_BAD_REQUEST)

            csv_request = CSVRequest(webhook_url=webhook_url)
            csv_request.save()

            for row in csv_reader:
                serial_no, product_name, input_urls = row
                
                ProductEntry.objects.create(
                    request=csv_request,
                    serial_no=int(serial_no),
                    product_name=product_name,
                    input_urls=input_urls
                )
                
                # # Save to database
                # processing_request = ImageProcessingRequest(
                #     serial_no=int(serial_no),
                #     product_name=product_name,
                #     input_urls=input_urls
                # )
                # processing_request.save()
                # Queue image processing task
            process_images.delay(str(csv_request.request_id))

            return Response({"request_id": str(csv_request.request_id)}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)