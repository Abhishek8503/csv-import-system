from django.urls import path
from .views import CSVUploadView, ImportJobStatusView, ImportJobRetryView

urlpatterns = [
    path("upload/", CSVUploadView.as_view(), name="csv-upload"),
    path("<int:job_id>/", ImportJobStatusView.as_view(), name="import-status"),
    path("<int:job_id/", ImportJobRetryView.as_view(), name="import-retry"),
]
