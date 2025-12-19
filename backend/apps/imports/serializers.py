from rest_framework import serializers
from .models import ImportJob

class ImportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportJob
        # fields = "__all__"
        fields = [
            "id",
            "status",
            "total_rows",
            "processed_rows",
            "progress_percent",
            "error_message",
            "created_at",
            "updated_at",
        ]

        def get_progress_percent(self, obj):
            if not obj.total_rows:
                return 0
            return int((obj.processed_rows)/(obj.total_rows)*100)
        