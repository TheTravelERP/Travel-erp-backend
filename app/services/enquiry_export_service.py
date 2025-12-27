# app/services/enquiry_export_service.py

from __future__ import annotations

import csv
from io import StringIO, BytesIO
from typing import List

from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.models.enquiry_model import Enquiry


# =========================
# CSV EXPORT
# =========================

def export_csv(rows: List[Enquiry]):
    def generate():
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow([
            "Customer Name",
            "Mobile",
            "Email",
            "Package",
            "Priority",
            "Status",
            "Created At"
        ])
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate(0)

        for r in rows:
            writer.writerow([
                r.customer_name,
                r.customer_mobile,
                r.customer_email,
                r.package_name,
                r.priority,
                r.conversion_status,
                r.created_at.strftime("%Y-%m-%d"),
            ])
            yield buffer.getvalue()
            buffer.seek(0)
            buffer.truncate(0)

    return StreamingResponse(
        generate(),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=enquiries.csv"
        }
    )


# =========================
# EXCEL EXPORT
# =========================

def export_excel(rows: List[Enquiry]):
    wb = Workbook()
    ws = wb.active
    ws.title = "Enquiries"

    ws.append([
        "Customer Name",
        "Mobile",
        "Email",
        "Package",
        "Priority",
        "Status",
        "Created At"
    ])

    for r in rows:
        ws.append([
            r.customer_name,
            r.customer_mobile,
            r.customer_email,
            r.package_name,
            r.priority,
            r.conversion_status,
            r.created_at.strftime("%Y-%m-%d"),
        ])

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)

    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=enquiries.xlsx"
        }
    )


# =========================
# PDF EXPORT
# =========================

def export_pdf(rows: List[Enquiry]):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    y = 800
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, y, "Enquiries Report")
    y -= 30

    c.setFont("Helvetica", 10)

    for r in rows:
        c.drawString(
            30, y,
            f"{r.customer_name} | {r.customer_mobile} | {r.priority}"
        )
        y -= 15
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = 800

    c.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=enquiries.pdf"
        }
    )
