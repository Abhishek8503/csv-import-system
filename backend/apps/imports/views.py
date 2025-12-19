from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ImportJob
from .serializers import ImportJobStatusSerializer, ImportJobCreateSerializer
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
        serializer = ImportJobCreateSerializer(import_job)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ImportJobStatusView(APIView):
    def get(self, request, job_id):
        job = get_object_or_404(ImportJob, id=job_id)
        serializer = ImportJobStatusSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ImportJobRetryView(APIView):
    def post(self, request, job_id):
        job = get_object_or_404(ImportJob, id=job_id)

        if job.status != ImportJob.Status.FAILED:
            return Response(
                {"error": "Only failed jobs can be retried"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        job.status = ImportJob.Status.PENDING
        job.error_message = ""
        job.processed_rows = 0
        job.save(update_fields=["status", "error_message", "processed_rows"])

        process_csv_import.delay(job.id)
        return Response({"message": "Retry Started"}, status=status.HTTP_202_ACCEPTED)