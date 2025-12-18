import csv
from celery import shared_task
from decimal import Decimal
import time
from django.db import transaction

from .models import ImportJob
from apps.products.models import Product

# @shared_task
# def test_background_task():
#     time.sleep(5)
#     return "Task Completed"

@shared_task(bind=True)
def process_csv_import(self, import_job_id):
    job = ImportJob.objects.get(id=import_job_id)

    try:
        job.status = ImportJob.Status.PROCESSING
        job.save(update_fields=["status"])

        file_path = job.file.path

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            
            rows = list(reader)
            total_rows = len(rows)
            job.total_rows = total_rows
            job.save(update_fields=["total_rows"])

            BATCH_SIZE = 1000
            batch = []

            for index, row in enumerate(rows, start=1):
                sku = row.get("sku", "").strip()
                name = row.get("name", "").strip()
                price = row.get("price", "0").strip()

                if not sku:
                    continue

                try:
                    price = Decimal(price)
                except Exception:
                    price = Decimal("0.00")

                sku_normalized = sku.lower()
                product = Product(
                    sku = sku_normalized,
                    name = name,
                    price = price,
                )

                batch.append(product)

                if len(batch) >= BATCH_SIZE:
                    _bulk_upsert_products(batch)
                    batch.clear()

                    job.processed_rows = index
                    job.save(update_fields=["processed_rows"])

            if batch:
                _bulk_upsert_products(batch)
                job.processed_rows = total_rows
                job.save(update_fields=["processed_rows"])
        
        job.status = ImportJob.Status.COMPLETED
        job.save(update_fields=["status"])
    
    except Exception as e:
        job.status = ImportJob.Status.FAILED
        job.error_message = str(e)
        job.save(update_fields=["status", "error_message"])
        raise


def _bulk_upsert_products(products):
    with transaction.atomic():
        Product.objects.bulk_create(
            products,
            ignore_conflicts=True,
            batch_size=1000
        )