#!/usr/bin/env python3
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(BASE_DIR, "external_files"), exist_ok=True)
PDF_PATH = os.path.join(BASE_DIR, "external_files", "google-store_audit_report.pdf")

doc = SimpleDocTemplate(PDF_PATH, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
styles = getSampleStyleSheet()

t_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#1a73e8'), spaceAfter=6)
sub_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=9, leading=12, textColor=colors.HexColor('#64748b'), spaceAfter=12)
h1_style = ParagraphStyle('DocH1', parent=styles['Heading2'], fontSize=12, leading=15, textColor=colors.HexColor('#0f172a'), spaceBefore=10, spaceAfter=4, keepWithNext=True)
body_style = ParagraphStyle('DocBody', parent=styles['Normal'], fontSize=9, leading=13, textColor=colors.HexColor('#334155'), spaceAfter=8)
box_style = ParagraphStyle('DocBox', parent=styles['Normal'], fontSize=8.5, leading=12, textColor=colors.HexColor('#1e293b'), backColor=colors.HexColor('#f8fafc'), borderPadding=6, spaceAfter=8)
alert_style = ParagraphStyle('DocAlert', parent=styles['Normal'], fontSize=8.5, leading=12, textColor=colors.HexColor('#991b1b'), backColor=colors.HexColor('#fee2e2'), borderPadding=6, spaceAfter=8)

elements = []

# ==================== PAGE 1 ====================
elements.append(Paragraph("Google Store — Hardware Quality Assurance Audit Report", t_style))
elements.append(Paragraph("<b>Component Audit Reference</b>: QA-AUD-2026-DISP904 | <b>Classification</b>: Confidential / Internal Operations", sub_style))
elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1a73e8'), spaceAfter=12))

# Metadata Table
meta_data = [
    ["Target Device:", "Pixel 11 Pro 256GB Obsidian (SKU-PX11P-256-OBS)", "Audit Period:", "August 1 – August 25, 2026"],
    ["Assembly Facility:", "Foxconn / Compal Precision Electronics (Tainan Plant)", "Destination DC:", "Tilburg Central DC (NL-TILBURG-01)"],
    ["Inspected Lot:", "Super Actua OLED Display (Sub-lot DISP-P11-904)", "Batch Volume:", "50,000 Display Assemblies"]
]
t_meta = Table(meta_data, colWidths=[95, 175, 90, 170])
t_meta.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
    ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#1e293b')),
    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
]))
elements.append(t_meta)
elements.append(Spacer(1, 14))

elements.append(Paragraph("1. Executive Summary & Audit Scope", h1_style))
elements.append(Paragraph("This factory acceptance quality audit evaluates 50,000 Super Actua OLED display assemblies manufactured for Google Pixel 11 Pro (SKU-PX11P-256-OBS) at the Tainan assembly plant between August 1 and August 25, 2026. All manufactured consignments were dispatched to European Central Distribution in Tilburg, Netherlands (NL-TILBURG-01) to support launch preorder fulfillment across Spain, France, Germany, Italy, and the United Kingdom.", body_style))

elements.append(Paragraph("2. Assembly Line Testing Methodology & Automated Test Equipment (ATE)", h1_style))
elements.append(Paragraph("Factory automated test equipment (ATE) evaluates display luminance uniformity, color accuracy (Delta E < 1.0), touch digitizer responsiveness, and pulse-width modulation (PWM) duty cycles across five brightness regimes (100%, 75%, 50%, 25%, and 10%). Standard factory gate acceptance criteria permit a maximum component failure rate of 1.5% across tested samples prior to containerized air freight dispatch.", body_style))

elements.append(Paragraph("3. Micro-Flicker Anomaly & Calibration Variance", h1_style))
elements.append(Paragraph("During secondary quality inspection at the factory gate, display sub-lot DISP-P11-904 exhibited an initial variance in high-frequency PWM driver pulse stability below 30% display brightness. While automated factory testing initially registered a minor variance of 1.2%, subsequent European field repair center intake records from B2X Frankfurt and CTDI Madrid have reported a verified customer defect rate of 9.6% on European preorder units.", body_style))
elements.append(Paragraph("<b>Preliminary Root Cause:</b> Component lot DISP-P11-904 utilized a secondary batch of power-management integrated circuits (PMIC) with tighter impedance tolerances, resulting in pulse timing drift under low-light operating temperatures.", alert_style))

# ==================== PAGE BREAK ====================
elements.append(PageBreak())

# ==================== PAGE 2 ====================
elements.append(Paragraph("Google Store — Hardware Quality Assurance Audit Report (Cont.)", t_style))
elements.append(Paragraph("<b>Section 4: Factory Gate Testing vs. European DC Intake Reconciliation</b>", h1_style))
elements.append(Paragraph("The following table reconciles factory gate test measurements against verified intake defect rates recorded at European authorized service centers (B2X Frankfurt and CTDI Madrid) across display sub-lots:", body_style))

table_data = [
    ["Component Lot ID", "Assembly Line", "Factory ATE Variance", "European DC Verified Defect Rate", "Discrepancy Status"],
    ["DISP-P11-901", "Line A-1", "0.4%", "0.6%", "CONFIRMED_NOMINAL"],
    ["DISP-P11-902", "Line A-2", "0.5%", "0.7%", "CONFIRMED_NOMINAL"],
    ["DISP-P11-903", "Line B-1", "0.8%", "1.1%", "CONFIRMED_NOMINAL"],
    ["DISP-P11-904", "Line B-3", "1.2%", "9.6% (Critical Mismatch)", "FLAGGED_CRITICAL_VARIANCE"],
    ["DISP-P11-905", "Line C-1", "0.6%", "0.8%", "CONFIRMED_NOMINAL"]
]

t_discrepancy = Table(table_data, colWidths=[95, 85, 110, 130, 110])
t_discrepancy.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#ffffff')),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    # Highlight row 4 (DISP-P11-904) in subtle light red
    ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#fee2e2')),
    ('TEXTCOLOR', (0,4), (-1,4), colors.HexColor('#991b1b')),
    ('FONTNAME', (0,4), (-1,4), 'Helvetica-Bold'),
]))
elements.append(t_discrepancy)
elements.append(Spacer(1, 14))

elements.append(Paragraph("5. Recommended Remediation & Containment Actions", h1_style))
elements.append(Paragraph("Based on the 8.4% calibration variance between factory gate testing (1.2%) and European verified service intake (9.6%), the Quality Engineering team mandates the following immediate actions:", body_style))
elements.append(Paragraph("• <b>Immediate Inventory Quarantine</b>: Quarantine all remaining unallocated factory inventory of display sub-lot DISP-P11-904 at the Tainan facility.<br/>• <b>Cross-Source RMA Reconciliation</b>: Reconcile European customer warranty return tickets (RMA-2026-0401 through RMA-2026-0410) with factory serial number manifests to confirm affected units.<br/>• <b>Firmware Mitigation Deployment</b>: Accelerate the rollout of firmware OTA patch OT-P11-26.2 to recalibrate the PWM duty cycle for low-luminance thresholds.<br/>• <b>Proactive Customer Service Recovery</b>: Issue €50 Google Store promotional vouchers alongside expedited warranty device replacements for affected European preorder customers.", box_style))

elements.append(Spacer(1, 10))
elements.append(Paragraph("6. Audit Sign-Off & Approvals", h1_style))
sign_data = [
    ["Lead Quality Auditor:", "Dr. H. Chen, Senior Director of Hardware QA", "Signature:", "[VERIFIED DIGITAL SIGNATURE]"],
    ["European Operations Lead:", "Google Store Hardware Operations Manager", "Date:", "September 18, 2026"]
]
t_sign = Table(sign_data, colWidths=[120, 160, 80, 170])
t_sign.setStyle(TableStyle([
    ('FONTSIZE', (0,0), (-1,-1), 7.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('LINEBELOW', (1,0), (1,0), 0.5, colors.HexColor('#64748b')),
    ('LINEBELOW', (3,0), (3,0), 0.5, colors.HexColor('#64748b')),
    ('LINEBELOW', (1,1), (1,1), 0.5, colors.HexColor('#64748b')),
    ('LINEBELOW', (3,1), (3,1), 0.5, colors.HexColor('#64748b')),
]))
elements.append(t_sign)

doc.build(elements)
print("✅ Successfully generated 2-page PDF: " + PDF_PATH)
