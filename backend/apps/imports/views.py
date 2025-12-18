from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ImportJob
from .serializers import ImportJobSerializer
from .tasks import process_csv_import
# Create your views here.

class CSVUploadView(APIView):
    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "CSV File is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        import_job = ImportJob.objects.create(file=file)
        process_csv_import.delay(import_job.id)
        serializer = ImportJobSerializer(import_job)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
