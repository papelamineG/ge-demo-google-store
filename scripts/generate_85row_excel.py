#!/usr/bin/env python3
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import random

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Carrier_Exception_Ledger"

# Styling
title_font = Font(name="Calibri", size=14, bold=True, color="1E293B")
kpi_label_font = Font(name="Calibri", size=9, bold=True, color="64748B")
kpi_val_font = Font(name="Calibri", size=11, bold=True, color="0F172A")
header_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
data_font = Font(name="Calibri", size=9, color="334155")
flag_font = Font(name="Calibri", size=9, bold=True, color="991B1B")

header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
kpi_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
alert_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

# Title
ws.merge_cells("A1:G1")
ws["A1"] = "Google Store Europe — Carrier Exceptions & Customs Hold Ledger (Launch Preorders)"
ws["A1"].font = title_font
ws["A1"].alignment = Alignment(vertical="center")
ws.row_dimensions[1].height = 30

# KPIs Row
kpis = [
    ("Total Consignments Tracked", "85"),
    ("Customs Exception Rate", "14.1%"),
    ("Pending Customs Release", "12"),
    ("At-Risk Preorder Revenue", "€48,200"),
    ("Courier SLA Penalty Accrued", "€12,450"),
    ("Audit Window", "Sept 2026 Launch"),
    ("Reconciliation Status", "FLAGGED_ACTION_REQUIRED")
]

for col_idx, (lbl, val) in enumerate(kpis, start=1):
    c_lbl = ws.cell(row=3, column=col_idx, value=lbl)
    c_lbl.font = kpi_label_font
    c_lbl.fill = kpi_fill
    c_lbl.alignment = Alignment(horizontal="center", vertical="center")
    c_lbl.border = thin_border
    
    c_val = ws.cell(row=4, column=col_idx, value=val)
    c_val.font = kpi_val_font
    c_val.fill = kpi_fill
    c_val.alignment = Alignment(horizontal="center", vertical="center")
    c_val.border = thin_border

ws.row_dimensions[3].height = 18
ws.row_dimensions[4].height = 22

# Headers Row
headers = [
    "Order_Reference", "Tracking_Number", "Destination_Country", 
    "Courier_Partner", "Manifest_Status", "Exception_Reason", "Action_Required"
]

for col_idx, h in enumerate(headers, start=1):
    c = ws.cell(row=6, column=col_idx, value=h)
    c.font = header_font
    c.fill = header_fill
    c.alignment = Alignment(horizontal="center", vertical="center")
    c.border = thin_border

ws.row_dimensions[6].height = 24

# Data Rows (Exactly 85 shipments)
# 12 Customs Holds (Rows 1 to 12)
flagged_rows = [
    ("ORD-2026-8701", "DHL-8701-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "UN3481 Lithium battery safety paperwork discrepancy at Brussels Air Hub", "Submit amended dangerous goods declaration"),
    ("ORD-2026-8702", "DHL-8702-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "UN3481 Lithium battery safety paperwork discrepancy at Brussels Air Hub", "Submit amended dangerous goods declaration"),
    ("ORD-2026-8703", "DHL-8703-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "Pallet dimension mismatch on consolidation manifest", "Issue re-manifesting order"),
    ("ORD-2026-8707", "DHL-8707-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "UN3481 Lithium battery safety paperwork discrepancy at Brussels Air Hub", "Submit amended dangerous goods declaration"),
    ("ORD-2026-8710", "DHL-8710-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "Held at Madrid Barajas airport sorting facility", "Priority courier clearance requested"),
    ("ORD-2026-8712", "DHL-8712-EU", "Spain (ES)", "DHL Express", "ESCALATED", "Customer reported transit damage outer carton and screen defect", "Initiate RMA return and courier insurance claim"),
    ("ORD-2026-8718", "DHL-8718-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "UN3481 Lithium battery safety paperwork discrepancy at Brussels Air Hub", "Submit amended dangerous goods declaration"),
    ("ORD-2026-8722", "DHL-8722-EU", "France (FR)", "DHL Express", "CUSTOMS_HOLD", "Roissy Charles de Gaulle airport customs clearance inspection", "Submit commercial invoice copy"),
    ("ORD-2026-8727", "DHL-8727-EU", "Germany (DE)", "DHL Express", "CUSTOMS_HOLD", "Leipzig Air Hub dangerous goods audit check", "Submit amended dangerous goods declaration"),
    ("ORD-2026-8731", "DHL-8731-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "UN3481 Lithium battery safety paperwork discrepancy at Brussels Air Hub", "Submit amended dangerous goods declaration"),
    ("ORD-2026-8735", "DHL-8735-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "UN3481 Lithium battery safety paperwork discrepancy at Brussels Air Hub", "Submit amended dangerous goods declaration"),
    ("ORD-2026-8740", "DPD-8740-EU", "Italy (IT)", "DPD Europe", "CUSTOMS_HOLD", "Transit documentation review at Milan hub", "Carrier customer service escalation")
]

# 73 Nominal Shipments (Rows 13 to 85)
countries = ["Spain (ES)", "France (FR)", "Germany (DE)", "Italy (IT)", "United Kingdom (UK)"]
couriers = ["DHL Express", "DPD Europe", "UPS"]
statuses = ["DELIVERED", "IN_TRANSIT", "OUT_FOR_DELIVERY", "CLEARED_CUSTOMS"]

all_rows = list(flagged_rows)

random.seed(42) # Deterministic
for i in range(13, 86):
    order_id = f"ORD-2026-{8740 + i}"
    courier = random.choice(couriers)
    tracking = f"{courier[:3].upper()}-{8740 + i}-EU"
    country = random.choice(countries)
    status = random.choice(statuses)
    reason = "Nominal transit on schedule" if status != "DELIVERED" else "Delivered to customer with signed POD"
    action = "None - standard delivery monitoring" if status != "DELIVERED" else "Completed"
    all_rows.append((order_id, tracking, country, courier, status, reason, action))

for row_idx, r_data in enumerate(all_rows, start=7):
    is_hold = "HOLD" in r_data[4] or "ESCALATED" in r_data[4]
    for col_idx, val in enumerate(r_data, start=1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.font = flag_font if (is_hold and col_idx == 5) else data_font
        cell.border = thin_border
        if is_hold:
            cell.fill = alert_fill
        elif row_idx % 2 == 0:
            cell.fill = zebra_fill
        if col_idx in (1, 2, 4, 5):
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.alignment = Alignment(vertical="center")
    ws.row_dimensions[row_idx].height = 18

# Set column widths
ws.column_dimensions['A'].width = 16
ws.column_dimensions['B'].width = 18
ws.column_dimensions['C'].width = 18
ws.column_dimensions['D'].width = 16
ws.column_dimensions['E'].width = 18
ws.column_dimensions['F'].width = 44
ws.column_dimensions['G'].width = 38

import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(base_dir, "external_files"), exist_ok=True)
out_path = os.path.join(base_dir, "external_files", "google-store_external_ledger.xlsx")
wb.save(out_path)
print(f"✅ Generated verified 85-row Excel ledger: {out_path} (Total rows in sheet: {ws.max_row})")
