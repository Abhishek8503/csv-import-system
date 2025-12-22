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
            if "sku" not in reader.fieldnames:
                raise ValueError("CSV Must Contain a 'sku' column.")
            rows = list(reader)
        total_rows = len(rows)
        job.total_rows = total_rows
        job.processed_rows = 0
        job.save(update_fields=["total_rows", "processed_rows"])

        BATCH_SIZE = 1000
        batch = []
        processed = 0

        for row in rows:
            sku = row.get("sku", "").strip()
            name = row.get("name", "").strip()
            price = row.get("price", "0").strip()

            if not sku:
                continue

            sku_normalized = sku.lower()
            product = Product(
                sku = sku_normalized,
                name = name,
                price = price or 0,
            )
            
            batch.append(product)
            processed += 1

            if len(batch) >= BATCH_SIZE:
                _bulk_upsert_products(batch)
                batch.clear()

                job.processed_rows = processed
                job.save(update_fields=["processed_rows"])

            # try:
            #     price = Decimal(price)
            # except Exception:
            #     price = Decimal("0.00")


        if batch:
            _bulk_upsert_products(batch)

        job.processed_rows = total_rows
        job.status = ImportJob.Status.COMPLETED
        job.save(update_fields=["processed_rows", "status"])
    
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