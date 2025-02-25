from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import csv
import uuid
from processing.tasks import long_running_task

class UploadView(APIView):
    def get(self, request):
        return Response(data={"message": "456454"}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            if "file" in request.FILES:
                file = request.FILES["file"]

            # Read the uploaded CSV file
            # csv_data = csv.reader(file.read().decode("utf-8").splitlines())

            # Process CSV data
            # rows = []
            # for row in csv_data:
            #     rows.append(row)  # You can process or save the row data here

            # Generate a unique ID for the background task
            unique_id = str(uuid.uuid4())

            # Trigger the Celery task asynchronously
            long_running_task.delay(unique_id)

            return Response(
                data={"uuid": unique_id}, status=status.HTTP_200_OK
            )

        except:
            import traceback

            print(traceback.format_exc())
            return Response(
                data={"error": "error hai"}, status=status.HTTP_400_BAD_REQUEST
            )
