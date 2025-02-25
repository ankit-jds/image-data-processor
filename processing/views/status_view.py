from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from processing.models import ImageProcessingRequest, CSVRequest, ProductEntry


class StatusView(APIView):
    def get(self, request, request_id=None):
        if request_id==None:
            return Response({"error": "request_id is missing"}, status=400)

        try:
            csv_request = CSVRequest.objects.get(request_id=request_id)
            entries = ProductEntry.objects.filter(request=csv_request)
            response_data = {
                "request_id": str(csv_request.request_id),
                "status": csv_request.status,
                "products": [
                    {
                        "serial_no": entry.serial_no,
                        "product_name": entry.product_name,
                        "input_urls": entry.input_urls,
                        "output_urls": entry.output_urls if csv_request.status == 'completed' else None
                    } for entry in entries
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Request ID not found"}, status=status.HTTP_404_NOT_FOUND)
   

