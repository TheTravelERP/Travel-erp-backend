import csv
from io import StringIO
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.models.enquiry_model import Enquiry


async def import_enquiries_from_csv(
    db: AsyncSession,
    org_id: int,
    user_id: int,
    file: UploadFile,
):
    content = await file.read()

    # Handle UTF-8 + BOM (Excel safe)
    text = content.decode("utf-8-sig")

    reader = csv.DictReader(StringIO(text))

    total = 0
    success = 0
    errors = []

    enquiries_to_insert = []

    for idx, row in enumerate(reader, start=2):  # header = row 1
        total += 1

        try:
            # ---------------- Required fields ----------------
            customer_name = row.get("customer_name", "").strip()
            customer_mobile = row.get("customer_mobile", "").strip()

            if not customer_name:
                raise ValueError("Customer name missing")

            if not customer_mobile:
                raise ValueError("Customer mobile missing")

            # ---------------- pax_count ----------------
            try:
                pax_count = int(row.get("pax_count", 1))
            except (ValueError, TypeError):
                pax_count = 1

            # ---------------- priority ----------------
            priority = (
                row.get("priority").strip()
                if row.get("priority") and row.get("priority").strip()
                else "Cold"
            )

            # ---------------- conversion_status ----------------
            conversion_status = (
                row.get("conversion_status").strip()
                if row.get("conversion_status") and row.get("conversion_status").strip()
                else "Pending"
            )

            # ---------------- lead_source (NOT NULL in DB) ----------------
            lead_source = (
                row.get("lead_source").strip()
                if row.get("lead_source") and row.get("lead_source").strip()
                else "Manual Import"
            )

            # ---------------- description ----------------
            description = (
                row.get("description").strip()
                if row.get("description") and row.get("description").strip()
                else None
            )

            # ---------------- quote_amount (NOT NULL in DB) ----------------
            try:
                quote_amount = float(row.get("quote_amount"))
            except (TypeError, ValueError):
                quote_amount = 0.0

            # ---------------- currency_code (NOT NULL in DB) ----------------
            currency_code = (
                row.get("currency_code").strip()
                if row.get("currency_code") and row.get("currency_code").strip()
                else "INR"
            )

            # ---------------- exchange_rate (NOT NULL in DB) ----------------
            try:
                exchange_rate = float(row.get("exchange_rate"))
            except (TypeError, ValueError):
                exchange_rate = 1.0

            enquiry = Enquiry(
                org_id=org_id,
                customer_name=customer_name,
                customer_mobile=customer_mobile,
                customer_email=row.get("customer_email"),
                package_name=row.get("package"),
                pax_count=pax_count,
                lead_source=lead_source,
                priority=priority,
                conversion_status=conversion_status,
                description=description,
                quote_amount=quote_amount,
                currency_code=currency_code,
                exchange_rate=exchange_rate,
                created_by=user_id,
                updated_at=datetime.now(timezone.utc),
            )

            enquiries_to_insert.append(enquiry)
            success += 1

        except Exception as e:
            errors.append({
                "row": idx,
                "error": str(e),
            })

    # ---------------- Bulk insert ----------------
    if enquiries_to_insert:
        db.add_all(enquiries_to_insert)
        await db.commit()

    return {
        "total_rows": total,
        "imported": success,
        "failed": total - success,
        "errors": errors,
    }
