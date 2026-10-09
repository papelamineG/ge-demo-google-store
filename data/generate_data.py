#!/usr/bin/env python3
"""
Synthetic Data Generator for Google Store Hardware Operations Demo.
Generates:
  - products_catalog.csv, products_catalog_schema.json, products_catalog_description.txt
  - hub_inventory.csv, hub_inventory_schema.json, hub_inventory_description.txt
  - customer_orders.csv, customer_orders_schema.json, customer_orders_description.txt
  - rma_defect_records.csv, rma_defect_records_schema.json, rma_defect_records_description.txt
  - firestore_seed.json
  - external_files_spec.json
"""

import os
import csv
import json
import random
from datetime import datetime, timedelta

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. PRODUCTS CATALOG
products = [
    ("SKU-PX11-128-OBS", "Pixel 11 128GB Obsidian", "Pixel Smartphone", "Obsidian", "128GB", 899.00, 24, "Tier 1 Priority"),
    ("SKU-PX11-256-POR", "Pixel 11 256GB Porcelain", "Pixel Smartphone", "Porcelain", "256GB", 999.00, 24, "Tier 1 Priority"),
    ("SKU-PX11-256-LEM", "Pixel 11 256GB Lemongrass", "Pixel Smartphone", "Lemongrass", "256GB", 999.00, 24, "Tier 1 Priority"),
    ("SKU-PX11P-256-OBS", "Pixel 11 Pro 256GB Obsidian", "Pixel Smartphone", "Obsidian", "256GB", 1199.00, 24, "Tier 1 Priority"),
    ("SKU-PX11P-256-POR", "Pixel 11 Pro 256GB Porcelain", "Pixel Smartphone", "Porcelain", "256GB", 1199.00, 24, "Tier 1 Priority"),
    ("SKU-PX11P-512-HAZ", "Pixel 11 Pro 512GB Hazel", "Pixel Smartphone", "Hazel", "512GB", 1329.00, 24, "Tier 1 Priority"),
    ("SKU-PX11P-1TB-OBS", "Pixel 11 Pro 1TB Obsidian", "Pixel Smartphone", "Obsidian", "1TB", 1589.00, 24, "Tier 1 Priority"),
    ("SKU-PX11PF-256-OBS", "Pixel 11 Pro Fold 256GB Obsidian", "Pixel Smartphone", "Obsidian", "256GB", 1899.00, 24, "Tier 1 Priority"),
    ("SKU-PX11PF-512-POR", "Pixel 11 Pro Fold 512GB Porcelain", "Pixel Smartphone", "Porcelain", "512GB", 2029.00, 24, "Tier 1 Priority"),
    ("SKU-PW5-41-BT-OBS", "Pixel Watch 5 41mm Bluetooth/Wi-Fi Obsidian", "Pixel Watch", "Matte Black", "41mm", 399.00, 24, "Tier 1 Priority"),
    ("SKU-PW5-41-LTE-POR", "Pixel Watch 5 41mm 4G LTE Porcelain", "Pixel Watch", "Polished Silver", "41mm", 449.00, 24, "Tier 1 Priority"),
    ("SKU-PW5-45-BT-HAZ", "Pixel Watch 5 45mm Bluetooth/Wi-Fi Hazel", "Pixel Watch", "Matte Hazel", "45mm", 449.00, 24, "Tier 1 Priority"),
    ("SKU-PW5-45-LTE-OBS", "Pixel Watch 5 45mm 4G LTE Obsidian", "Pixel Watch", "Matte Black", "45mm", 499.00, 24, "Tier 1 Priority"),
    ("SKU-PBP3-OBS", "Pixel Buds Pro 3 Obsidian", "Audio", "Obsidian", "Standard", 249.00, 24, "Tier 1 Priority"),
    ("SKU-PBP3-POR", "Pixel Buds Pro 3 Porcelain", "Audio", "Porcelain", "Standard", 249.00, 24, "Tier 1 Priority"),
    ("SKU-PBP3-WIN", "Pixel Buds Pro 3 Wintergreen", "Audio", "Wintergreen", "Standard", 249.00, 24, "Tier 1 Priority"),
    ("SKU-NST-LRN-4G", "Nest Learning Thermostat 4th Gen Polished Silver", "Smart Home", "Polished Silver", "Standard", 329.00, 24, "General Availability"),
    ("SKU-GTV-STR-4K", "Google TV Streamer 4K Porcelain", "Smart Home", "Porcelain", "32GB", 119.00, 24, "General Availability"),
    ("SKU-CHG-45W-USB", "45W USB-C Power Adapter White", "Accessories", "White", "45W", 39.00, 12, "General Availability"),
    ("SKU-CAS-PX11P-OBS", "Pixel 11 Pro Protective Case Obsidian", "Accessories", "Obsidian", "Standard", 45.00, 12, "General Availability"),
    ("SKU-CAS-PX11P-POR", "Pixel 11 Pro Protective Case Porcelain", "Accessories", "Porcelain", "Standard", 45.00, 12, "General Availability"),
    ("SKU-BND-PW5-ACT-OBS", "Pixel Watch 5 Active Band Obsidian", "Accessories", "Obsidian", "Active Sport", 59.00, 12, "General Availability"),
]

# Write products_catalog.csv
with open(os.path.join(DATA_DIR, "products_catalog.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["sku_id", "product_name", "product_family", "color_finish", "storage_capacity", "msrp_eur", "warranty_months", "launch_tier"])
    for p in products:
        writer.writerow(p)

with open(os.path.join(DATA_DIR, "products_catalog_description.txt"), "w", encoding="utf-8") as f:
    f.write("Master catalog of Google hardware devices, smartphones, smartwatches, smart home, and official accessories sold on store.google.com with retail MSRP in Euro.\n")

products_schema = [
    {"name": "sku_id", "type": "STRING", "description": "Unique Google hardware product SKU code (PK, e.g. SKU-PX11P-256-OBS)"},
    {"name": "product_name", "type": "STRING", "description": "Commercial product model name (e.g. Pixel 11 Pro 256GB Obsidian)"},
    {"name": "product_family", "type": "STRING", "description": "Hardware category (Pixel Smartphone, Pixel Watch, Audio, Smart Home, Accessories)"},
    {"name": "color_finish", "type": "STRING", "description": "Factory colorway and finish (Obsidian, Porcelain, Hazel, Lemongrass)"},
    {"name": "storage_capacity", "type": "STRING", "description": "Internal storage capacity or size (128GB, 256GB, 512GB, 1TB, 41mm, 45mm)"},
    {"name": "msrp_eur", "type": "FLOAT", "description": "Official retail launch price in Euro (EUR €)"},
    {"name": "warranty_months", "type": "INTEGER", "description": "Standard manufacturer hardware warranty duration in months"},
    {"name": "launch_tier", "type": "STRING", "description": "Product launch priority tier (Tier 1 Priority, General Availability)"}
]
with open(os.path.join(DATA_DIR, "products_catalog_schema.json"), "w", encoding="utf-8") as f:
    json.dump(products_schema, f, indent=2)


# 2. HUB INVENTORY
hubs = [
    ("NL-TILBURG-01", "Tilburg European Central Distribution Center", "NL", "Tilburg"),
    ("IE-DUBLIN-02", "Dublin Western Europe Logistics Hub", "IE", "Dublin"),
    ("DE-FRANKFURT-01", "Frankfurt Central Regional Hub", "DE", "Frankfurt"),
    ("ES-MADRID-01", "Madrid Southern Europe Hub", "ES", "Madrid"),
]

inventory_rows = []
inv_id_counter = 1001

for hub_code, hub_name, country_code, city in hubs:
    for prod in products:
        sku = prod[0]
        # Specific crisis scenario for Pixel 11 Pro Obsidian and Pixel Watch 5 LTE in Tilburg
        if hub_code == "NL-TILBURG-01" and sku == "SKU-PX11P-256-OBS":
            on_hand = 1250
            reserved = 1680
            safety = 500
            status = "CRITICAL_BACKORDER"
            lead_days = 6
        elif hub_code == "NL-TILBURG-01" and sku == "SKU-PW5-45-LTE-OBS":
            on_hand = 420
            reserved = 580
            safety = 200
            status = "CRITICAL_BACKORDER"
            lead_days = 5
        elif hub_code == "IE-DUBLIN-02" and sku == "SKU-PX11P-256-OBS":
            on_hand = 920
            reserved = 410
            safety = 250
            status = "HEALTHY" # Surplus available for inter-hub transfer!
            lead_days = 3
        elif hub_code == "DE-FRANKFURT-01" and sku == "SKU-PX11P-256-OBS":
            on_hand = 680
            reserved = 320
            safety = 200
            status = "HEALTHY"
            lead_days = 2
        else:
            on_hand = random.randint(300, 1800)
            reserved = random.randint(150, int(on_hand * 0.75))
            safety = random.randint(100, 300)
            status = "HEALTHY" if on_hand - reserved > safety else "CONSTRAINED"
            lead_days = random.randint(2, 5)

        inventory_rows.append([
            f"INV-{inv_id_counter}",
            hub_code,
            hub_name,
            country_code,
            sku,
            on_hand,
            reserved,
            safety,
            lead_days,
            status
        ])
        inv_id_counter += 1

with open(os.path.join(DATA_DIR, "hub_inventory.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["inventory_id", "hub_code", "hub_name", "country_code", "sku_id", "on_hand_stock", "reserved_preorders", "safety_threshold", "replenishment_lead_days", "stock_status"])
    for r in inventory_rows:
        writer.writerow(r)

with open(os.path.join(DATA_DIR, "hub_inventory_description.txt"), "w", encoding="utf-8") as f:
    f.write("Fulfillment warehouse stock and launch preorder reservation levels across European distribution centers for Google Store.\n")

inventory_schema = [
    {"name": "inventory_id", "type": "STRING", "description": "Inventory ledger identifier (PK, e.g. INV-1001)"},
    {"name": "hub_code", "type": "STRING", "description": "Fulfillment center facility code (NL-TILBURG-01, IE-DUBLIN-02, DE-FRANKFURT-01, ES-MADRID-01)"},
    {"name": "hub_name", "type": "STRING", "description": "Full logistics hub facility name"},
    {"name": "country_code", "type": "STRING", "description": "Facility country ISO code (NL, IE, DE, ES)"},
    {"name": "sku_id", "type": "STRING", "description": "Google Store hardware product SKU (FK to products_catalog.sku_id)"},
    {"name": "on_hand_stock", "type": "INTEGER", "description": "Physical unit inventory count present in warehouse shelves"},
    {"name": "reserved_preorders", "type": "INTEGER", "description": "Units allocated to pending customer preorders awaiting dispatch"},
    {"name": "safety_threshold", "type": "INTEGER", "description": "Minimum safety buffer stock threshold triggering replenishment"},
    {"name": "replenishment_lead_days", "type": "INTEGER", "description": "Estimated transit days required for stock replenishment"},
    {"name": "stock_status", "type": "STRING", "description": "Operational inventory health status (HEALTHY, CONSTRAINED, CRITICAL_BACKORDER)"}
]
with open(os.path.join(DATA_DIR, "hub_inventory_schema.json"), "w", encoding="utf-8") as f:
    json.dump(inventory_schema, f, indent=2)


# 3. CUSTOMER ORDERS
destinations = [
    ("ES", "Madrid", "DHL Express", "NL-TILBURG-01"),
    ("ES", "Barcelona", "DHL Express", "NL-TILBURG-01"),
    ("ES", "Valencia", "DPD Europe", "ES-MADRID-01"),
    ("ES", "Seville", "DHL Express", "ES-MADRID-01"),
    ("FR", "Paris", "DPD Europe", "NL-TILBURG-01"),
    ("FR", "Lyon", "DHL Express", "NL-TILBURG-01"),
    ("FR", "Marseille", "DPD Europe", "NL-TILBURG-01"),
    ("DE", "Berlin", "DHL Express", "DE-FRANKFURT-01"),
    ("DE", "Munich", "DHL Express", "DE-FRANKFURT-01"),
    ("DE", "Hamburg", "DPD Europe", "DE-FRANKFURT-01"),
    ("IT", "Milan", "UPS", "DE-FRANKFURT-01"),
    ("IT", "Rome", "UPS", "DE-FRANKFURT-01"),
    ("UK", "London", "DHL Express", "IE-DUBLIN-02"),
    ("UK", "Manchester", "DPD Europe", "IE-DUBLIN-02"),
]

orders_rows = []
base_date = datetime(2026, 8, 25, 10, 0, 0)

# Seed orders
order_id_counter = 8700

# High-priority orders affected by launch backorder & carrier customs hold
flagged_orders = [
    (8701, "SKU-PX11P-256-OBS", "ES", "Madrid", "DHL Express", "NL-TILBURG-01", "TRANSIT_DELAYED", 1199.00, "HIGH_PRIORITY_VIP"),
    (8702, "SKU-PX11P-256-OBS", "ES", "Barcelona", "DHL Express", "NL-TILBURG-01", "TRANSIT_DELAYED", 1199.00, "HIGH_PRIORITY_VIP"),
    (8703, "SKU-PW5-45-LTE-OBS", "ES", "Madrid", "DHL Express", "NL-TILBURG-01", "TRANSIT_DELAYED", 499.00, "STANDARD"),
    (8704, "SKU-PX11P-256-OBS", "FR", "Paris", "DPD Europe", "NL-TILBURG-01", "TRANSIT_DELAYED", 1199.00, "HIGH_PRIORITY_VIP"),
    (8705, "SKU-PX11PF-256-OBS", "FR", "Lyon", "DHL Express", "NL-TILBURG-01", "DELIVERED", 1899.00, "STANDARD"),
    (8706, "SKU-PX11P-256-OBS", "DE", "Munich", "DHL Express", "NL-TILBURG-01", "TRANSIT_DELAYED", 1199.00, "STANDARD"),
    (8707, "SKU-PX11P-256-OBS", "ES", "Valencia", "DHL Express", "NL-TILBURG-01", "TRANSIT_DELAYED", 1199.00, "HIGH_PRIORITY_VIP"),
    (8708, "SKU-PW5-45-LTE-OBS", "DE", "Berlin", "DHL Express", "NL-TILBURG-01", "TRANSIT_DELAYED", 499.00, "STANDARD"),
    (8709, "SKU-PX11P-512-HAZ", "ES", "Madrid", "DHL Express", "NL-TILBURG-01", "DELIVERED", 1329.00, "STANDARD"),
    (8710, "SKU-PX11P-256-OBS", "ES", "Seville", "DHL Express", "NL-TILBURG-01", "TRANSIT_DELAYED", 1199.00, "HIGH_PRIORITY_VIP"),
    (8711, "SKU-PX11P-256-OBS", "FR", "Paris", "DPD Europe", "NL-TILBURG-01", "PENDING_INSPECTION", 1199.00, "STANDARD"),
    (8712, "SKU-PX11P-256-OBS", "ES", "Madrid", "DHL Express", "NL-TILBURG-01", "ESCALATED_DISPUTE", 1199.00, "HIGH_PRIORITY_VIP"),
]

for oid, sku, ctry, city, carrier, hub, status, amount, priority in flagged_orders:
    o_date = base_date + timedelta(days=random.randint(1, 5), hours=random.randint(1, 12))
    p_date = o_date + timedelta(days=4)
    orders_rows.append([
        f"ORD-2026-{oid}",
        f"CUST-EU-{random.randint(10000, 99999)}",
        sku,
        o_date.strftime("%Y-%m-%d %H:%M:%S"),
        p_date.strftime("%Y-%m-%d"),
        hub,
        ctry,
        city,
        carrier,
        f"{carrier[:3].upper()}-{oid}-EU",
        status,
        f"{amount:.2f}",
        priority
    ])

# Additional representative orders
prod_map = {p[0]: p[5] for p in products}
prod_skus = list(prod_map.keys())

for i in range(13, 120):
    oid = 8700 + i
    dest = random.choice(destinations)
    sku = random.choice(prod_skus)
    amt = prod_map[sku]
    o_date = base_date + timedelta(days=random.randint(1, 22), hours=random.randint(1, 14))
    p_date = o_date + timedelta(days=random.randint(3, 5))
    
    # 70% Delivered, 15% Shipped, 10% Allocated, 5% Delayed
    dice = random.random()
    if dice < 0.70:
        stat = "DELIVERED"
    elif dice < 0.85:
        stat = "SHIPPED"
    elif dice < 0.95:
        stat = "ALLOCATED"
    else:
        stat = "TRANSIT_DELAYED"

    orders_rows.append([
        f"ORD-2026-{oid}",
        f"CUST-EU-{random.randint(10000, 99999)}",
        sku,
        o_date.strftime("%Y-%m-%d %H:%M:%S"),
        p_date.strftime("%Y-%m-%d"),
        dest[3],
        dest[0],
        dest[1],
        dest[2],
        f"{dest[2][:3].upper()}-{oid}-EU",
        stat,
        f"{amt:.2f}",
        "HIGH_PRIORITY_VIP" if amt > 1200 else "STANDARD"
    ])

with open(os.path.join(DATA_DIR, "customer_orders.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["order_id", "customer_id", "sku_id", "order_placed_at", "promised_delivery_date", "fulfillment_hub", "destination_country", "shipping_city", "carrier_partner", "tracking_number", "order_status", "total_paid_eur", "priority_flag"])
    for r in orders_rows:
        writer.writerow(r)

with open(os.path.join(DATA_DIR, "customer_orders_description.txt"), "w", encoding="utf-8") as f:
    f.write("Individual customer hardware purchase orders, shipping destinations, courier tracking, and dispatch statuses on Google Store Europe.\n")

orders_schema = [
    {"name": "order_id", "type": "STRING", "description": "Unique Google Store customer order number (PK, e.g. ORD-2026-8701)"},
    {"name": "customer_id", "type": "STRING", "description": "Anonymized customer account identifier"},
    {"name": "sku_id", "type": "STRING", "description": "Ordered hardware model SKU (FK to products_catalog.sku_id)"},
    {"name": "order_placed_at", "type": "TIMESTAMP", "description": "Exact order placement timestamp"},
    {"name": "promised_delivery_date", "type": "DATE", "description": "Customer SLA promised delivery date"},
    {"name": "fulfillment_hub", "type": "STRING", "description": "Fulfillment center assigned to dispatch order (FK to hub_inventory.hub_code)"},
    {"name": "destination_country", "type": "STRING", "description": "Destination country ISO code (ES, FR, DE, IT, UK)"},
    {"name": "shipping_city", "type": "STRING", "description": "Destination shipping metropolitan city"},
    {"name": "carrier_partner", "type": "STRING", "description": "Assigned parcel logistics courier (DHL Express, DPD Europe, UPS)"},
    {"name": "tracking_number", "type": "STRING", "description": "Courier parcel tracking reference code"},
    {"name": "order_status", "type": "STRING", "description": "Order fulfillment state (DELIVERED, SHIPPED, ALLOCATED, TRANSIT_DELAYED, PENDING_INSPECTION, ESCALATED_DISPUTE)"},
    {"name": "total_paid_eur", "type": "FLOAT", "description": "Final customer transaction value in Euro (€)"},
    {"name": "priority_flag", "type": "STRING", "description": "Customer service priority classification (STANDARD, HIGH_PRIORITY_VIP)"}
]
with open(os.path.join(DATA_DIR, "customer_orders_schema.json"), "w", encoding="utf-8") as f:
    json.dump(orders_schema, f, indent=2)


# 4. RMA DEFECT RECORDS
rma_rows = [
    ["RMA-2026-0401", "ORD-2026-8712", "SKU-PX11P-256-OBS", "IMEI-35829104882101", "2026-09-02 14:15:00", "OLED_MICRO_FLICKER", "HIGH", "Customer reports noticeable screen flicker below 30% brightness near camera punch hole. Linked to Asian display lot DISP-P11-904.", "VERIFIED_HARDWARE_FAULT", "B2X European Repair Center (Frankfurt)", "1199.00", "FRUSTRATED"],
    ["RMA-2026-0402", "ORD-2026-8701", "SKU-PX11P-256-OBS", "IMEI-35829104882144", "2026-09-03 09:30:00", "OLED_MICRO_FLICKER", "HIGH", "Display flicker observed on grey backgrounds. Lot DISP-P11-904 calibration drift confirmed.", "VERIFIED_HARDWARE_FAULT", "B2X European Repair Center (Frankfurt)", "0.00", "ANXIOUS"],
    ["RMA-2026-0403", "ORD-2026-8703", "SKU-PW5-45-LTE-OBS", "SN-PW5-8829104-ES", "2026-09-04 11:20:00", "CERAMIC_SEAL_BREACH", "CRITICAL", "Moisture ingress detected behind bioactive sensor ceramic backplate during gym session.", "PENDING_TRIAGE", "CTDI Logistics & Repair (Madrid)", "0.00", "DISSATISFIED"],
    ["RMA-2026-0404", "ORD-2026-8707", "SKU-PX11P-256-OBS", "IMEI-35829104882199", "2026-09-05 16:45:00", "OLED_MICRO_FLICKER", "HIGH", "Intermittent green flash on lock screen unlock. Lot DISP-P11-904.", "VERIFIED_HARDWARE_FAULT", "B2X European Repair Center (Frankfurt)", "50.00", "FRUSTRATED"],
    ["RMA-2026-0405", "ORD-2026-8710", "SKU-PX11P-256-OBS", "IMEI-35829104882215", "2026-09-06 13:10:00", "OLED_MICRO_FLICKER", "HIGH", "Pulse width modulation instability. Verified by repair technician checklist.", "REPLACEMENT_DISPATCHED", "B2X European Repair Center (Frankfurt)", "0.00", "NEUTRAL"],
    ["RMA-2026-0406", "ORD-2026-8711", "SKU-PX11P-256-OBS", "IMEI-35829104882280", "2026-09-07 10:05:00", "BATTERY_CALIBRATION_DRIFT", "MEDIUM", "Battery percentage drops from 20% to 5% rapidly. Recalibration firmware update requested.", "PENDING_TRIAGE", "B2X European Repair Center (Frankfurt)", "0.00", "NEUTRAL"],
    ["RMA-2026-0407", "ORD-2026-8724", "SKU-PBP3-OBS", "SN-PBP3-991204-FR", "2026-09-08 15:40:00", "AUDIO_ANC_FEEDBACK", "LOW", "High frequency hiss in left earbud when Transparency mode engaged.", "REFUND_CREDITED", "CTDI Logistics & Repair (Paris)", "249.00", "SATISFIED"],
    ["RMA-2026-0408", "ORD-2026-8735", "SKU-PX11-128-OBS", "IMEI-35829105110482", "2026-09-09 12:00:00", "COSMETIC_BLEMISH", "LOW", "Minor scratch on aluminum frame out of retail packaging.", "REFUND_CREDITED", "B2X European Repair Center (Frankfurt)", "80.00", "SATISFIED"],
    ["RMA-2026-0409", "ORD-2026-8742", "SKU-PX11PF-256-OBS", "IMEI-35829106001294", "2026-09-10 17:25:00", "HINGE_RESISTANCE_VARIANCE", "MEDIUM", "Hinge opening angle exhibits friction resistance between 45 and 90 degrees.", "PENDING_TRIAGE", "B2X European Repair Center (Frankfurt)", "0.00", "ANXIOUS"],
    ["RMA-2026-0410", "ORD-2026-8750", "SKU-PW5-41-BT-OBS", "SN-PW5-8810294-DE", "2026-09-11 11:15:00", "HAPTIC_FEEDBACK_VARIANCE", "LOW", "Crown vibration motor feels muffled compared to store display model.", "REPLACEMENT_DISPATCHED", "B2X European Repair Center (Frankfurt)", "0.00", "SATISFIED"],
]

for i in range(11, 36):
    rma_id = f"RMA-2026-04{i:02d}"
    order_ref = f"ORD-2026-87{random.randint(15, 80):02d}"
    prod = random.choice(products[:12])
    sku = prod[0]
    is_flicker = (sku == "SKU-PX11P-256-OBS") and random.random() < 0.65
    cat = "OLED_MICRO_FLICKER" if is_flicker else random.choice(["BATTERY_CALIBRATION_DRIFT", "BLUETOOTH_DISCONNECTION", "COSMETIC_BLEMISH", "TOUCHSCREEN_LATENCY"])
    sev = "HIGH" if cat == "OLED_MICRO_FLICKER" else random.choice(["MEDIUM", "LOW"])
    summary = f"Technician intake scan notes: {cat.lower().replace('_', ' ')} detected during factory diagnostic cycle."
    stat = random.choice(["PENDING_TRIAGE", "VERIFIED_HARDWARE_FAULT", "REPLACEMENT_DISPATCHED", "REFUND_CREDITED"])
    center = random.choice(["B2X European Repair Center (Frankfurt)", "CTDI Logistics & Repair (Madrid)", "CTDI Logistics & Repair (Paris)"])
    voucher = f"{random.choice([0.0, 50.0, 80.0, 120.0]):.2f}"
    sentiment = random.choice(["FRUSTRATED", "ANXIOUS", "NEUTRAL", "SATISFIED"])
    date_str = (base_date + timedelta(days=random.randint(8, 24), hours=random.randint(8, 18))).strftime("%Y-%m-%d %H:%M:%S")

    rma_rows.append([
        rma_id,
        order_ref,
        sku,
        f"IMEI-35829104{random.randint(100000, 999999)}",
        date_str,
        cat,
        sev,
        summary,
        stat,
        center,
        voucher,
        sentiment
    ])

with open(os.path.join(DATA_DIR, "rma_defect_records.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["rma_id", "order_id", "sku_id", "serial_number", "incident_date", "defect_category", "defect_severity", "technician_diagnostic_summary", "triage_status", "assigned_repair_center", "refund_credit_eur", "customer_sentiment"])
    for r in rma_rows:
        writer.writerow(r)

with open(os.path.join(DATA_DIR, "rma_defect_records_description.txt"), "w", encoding="utf-8") as f:
    f.write("Warranty return authorizations, hardware defect diagnostics, and service center triage logs for Google Store devices.\n")

rma_schema = [
    {"name": "rma_id", "type": "STRING", "description": "Return Merchandise Authorization identifier (PK, e.g. RMA-2026-0401)"},
    {"name": "order_id", "type": "STRING", "description": "Associated Google Store customer order (FK to customer_orders.order_id)"},
    {"name": "sku_id", "type": "STRING", "description": "Hardware device SKU undergoing RMA evaluation (FK to products_catalog.sku_id)"},
    {"name": "serial_number", "type": "STRING", "description": "Device IMEI number or hardware serial code"},
    {"name": "incident_date", "type": "TIMESTAMP", "description": "Date and time when warranty return incident was logged"},
    {"name": "defect_category", "type": "STRING", "description": "Diagnostic root defect category (OLED_MICRO_FLICKER, BATTERY_CALIBRATION_DRIFT, CERAMIC_SEAL_BREACH, HAPTIC_FEEDBACK_VARIANCE)"},
    {"name": "defect_severity", "type": "STRING", "description": "Defect classification impact severity (LOW, MEDIUM, HIGH, CRITICAL)"},
    {"name": "technician_diagnostic_summary", "type": "STRING", "description": "Authorized repair technician diagnostic findings and observations"},
    {"name": "triage_status", "type": "STRING", "description": "Current RMA resolution stage (PENDING_TRIAGE, VERIFIED_HARDWARE_FAULT, REPLACEMENT_DISPATCHED, REFUND_CREDITED, REJECTED_CUSTOMER_DAMAGE)"},
    {"name": "assigned_repair_center", "type": "STRING", "description": "Certified European repair center handling inspection (B2X Frankfurt, CTDI Madrid, CTDI Paris)"},
    {"name": "refund_credit_eur", "type": "FLOAT", "description": "Processed financial compensation or Google Store goodwill voucher in Euro (€)"},
    {"name": "customer_sentiment", "type": "STRING", "description": "Assessed customer emotional sentiment during ticket escalation (SATISFIED, NEUTRAL, ANXIOUS, FRUSTRATED)"}
]
with open(os.path.join(DATA_DIR, "rma_defect_records_schema.json"), "w", encoding="utf-8") as f:
    json.dump(rma_schema, f, indent=2)


# 5. FIRESTORE SEED DATA
firestore_seed = [
    {
        "id": "task-launch-backorder-01",
        "data": {
            "task_id": "task-launch-backorder-01",
            "title": "Pixel 11 Pro 256GB Obsidian Launch Backorder at Tilburg DC",
            "issue_type": "INVENTORY_DEFICIT_BACKORDER",
            "risk_level": "CRITICAL",
            "current_status": "PENDING_APPROVAL",
            "workflow_state": "NEEDS_STOCK_REBALANCING",
            "owning_department": "Fulfillment_Operations",
            "target_sku": "SKU-PX11P-256-OBS",
            "target_hub": "NL-TILBURG-01",
            "deficit_units": 430,
            "recommended_action": "Execute inter-hub emergency stock transfer of 450 units from Dublin Hub (IE-DUBLIN-02) to Tilburg DC (NL-TILBURG-01) via express air charter.",
            "impact_eur": 515570.00,
            "audit_trail": [
                {"timestamp": "2026-09-18T08:00:00Z", "author": "system_monitoring_daemon", "event": "SLA violation alert triggered for 430 customer preorders."}
            ]
        }
    },
    {
        "id": "task-rma-display-flicker-02",
        "data": {
            "task_id": "task-rma-display-flicker-02",
            "title": "Display Flicker Defect Batch Triage on Lot DISP-P11-904",
            "issue_type": "HARDWARE_QUALITY_DISCREPANCY",
            "risk_level": "HIGH",
            "current_status": "IN_PROGRESS",
            "workflow_state": "SUPPLIER_AUDIT_RECONCILIATION",
            "owning_department": "Quality_Engineering",
            "target_sku": "SKU-PX11P-256-OBS",
            "target_hub": "DE-FRANKFURT-01",
            "affected_rma_count": 14,
            "recommended_action": "Correlate factory QA audit report against B2X repair records, isolate lot DISP-P11-904, and auto-authorize priority hardware replacements with €50 Store Vouchers.",
            "impact_eur": 16786.00,
            "audit_trail": [
                {"timestamp": "2026-09-18T10:15:00Z", "author": "b2x_quality_gateway", "event": "14 display flicker defect intake slips verified with PWM variance."}
            ]
        }
    },
    {
        "id": "task-carrier-customs-hold-03",
        "data": {
            "task_id": "task-carrier-customs-hold-03",
            "title": "DHL Express Customs Clearance Hold for 12 Madrid Preorder Consignments",
            "issue_type": "LOGISTICS_TRANSIT_EXCEPTION",
            "risk_level": "HIGH",
            "current_status": "PENDING_APPROVAL",
            "workflow_state": "CARRIER_ESCALATION_QUEUED",
            "owning_department": "Logistics_Partnerships",
            "target_sku": "MULTIPLE_LAUNCH_SKUS",
            "target_hub": "ES-MADRID-01",
            "held_orders": ["ORD-2026-8701", "ORD-2026-8702", "ORD-2026-8703", "ORD-2026-8707"],
            "recommended_action": "Transmit corrected UN3481 lithium battery flight safety declarations to DHL Brussels Air Hub to release held consignments within 4 hours.",
            "impact_eur": 48200.00,
            "audit_trail": [
                {"timestamp": "2026-09-18T11:45:00Z", "author": "dhl_edi_listener", "event": "Customs exception code EX-LITH-3481 raised on shipment manifest."}
            ]
        }
    },
    {
        "id": "task-watch-seal-audit-04",
        "data": {
            "task_id": "task-watch-seal-audit-04",
            "title": "Pixel Watch 5 Bio-Sensor Ceramic Seal Ingress Investigation",
            "issue_type": "SUPPLIER_TOLERANCE_AUDIT",
            "risk_level": "MEDIUM",
            "current_status": "ANALYZING",
            "workflow_state": "SAMPLE_INSPECTION",
            "owning_department": "Quality_Engineering",
            "target_sku": "SKU-PW5-45-LTE-OBS",
            "target_hub": "ES-MADRID-01",
            "affected_units": 3,
            "recommended_action": "Audit acoustic leak tester logs from Compal assembly line 4 and recalibrate incoming ultrasonic inspection at Madrid hub.",
            "impact_eur": 1497.00,
            "audit_trail": [
                {"timestamp": "2026-09-18T13:20:00Z", "author": "ctdi_intake_system", "event": "RMA-2026-0403 sensor ingress verified under hydrostatic test."}
            ]
        }
    },
    {
        "id": "task-carrier-sla-penalty-05",
        "data": {
            "task_id": "task-carrier-sla-penalty-05",
            "title": "DPD Europe Transit SLA Clawback Credit Calculation",
            "issue_type": "COMMERCIAL_SLA_RECONCILIATION",
            "risk_level": "LOW",
            "current_status": "COMPLETED",
            "workflow_state": "CREDIT_MEMO_POSTED",
            "owning_department": "Finance_Operations",
            "target_sku": "ALL_MODELS",
            "target_hub": "NL-TILBURG-01",
            "clawback_credit_eur": 12450.00,
            "recommended_action": "Apply contractual SLA penalty of €25 per delayed parcel against DPD monthly billing statement.",
            "impact_eur": 12450.00,
            "audit_trail": [
                {"timestamp": "2026-09-17T17:00:00Z", "author": "finance_reconciliation_bot", "event": "Credit memo CM-2026-0917-DPD confirmed and posted to SAP."}
            ]
        }
    }
]

with open(os.path.join(DATA_DIR, "firestore_seed.json"), "w", encoding="utf-8") as f:
    json.dump(firestore_seed, f, indent=2)


# 6. EXTERNAL FILES SPEC (PDF, EXCEL, SCANNED FORMS)
external_files_spec = {
    "style": {
        "company": "Google Store",
        "doc_type": "Hardware Quality & Logistics Audit",
        "primary_color": "#1a73e8",
        "font_family": "Helvetica"
    },
    "pdf": {
        "title": "Google Store - Asian Display Assembly Quality Audit Report (Lot DISP-P11-904)",
        "sections": [
            {
                "heading": "1. Executive Summary & Audit Scope",
                "content": "This audit covers factory acceptance testing for 50,000 Super Actua OLED display assemblies manufactured for Google Pixel 11 Pro (SKU-PX11P-256-OBS) at the Tainan assembly plant between August 1 and August 25, 2026. Shipments were consigned to European Central Distribution (Tilburg, Netherlands)."
            },
            {
                "heading": "2. High-Frequency Micro-Flicker Anomaly & Calibration Variance",
                "content": "During secondary quality inspection at the factory gate, display sub-lot DISP-P11-904 exhibited an 8.4% variance in pulse-width modulation (PWM) frequency stability below 30% display brightness. While factory automated test equipment (ATE) initially logged a 1.2% minor variance, European repair center (B2X Frankfurt) intake records report a verified failure rate of 9.6% on European customer preorders."
            },
            {
                "heading": "3. Cross-Source Reconciliation & Recommended Actions",
                "content": "1. Quarantine remaining factory inventory of display lot DISP-P11-904.\n2. Reconcile internal RMA tickets (RMA-2026-0401 through RMA-2026-0410) against factory calibration serial logs.\n3. Accelerate firmware patch release OT-P11-26.2 to adjust low-light PWM duty cycle.\n4. Proactively grant €50 Google Store promotional credits to affected Tier-1 preorder customers."
            }
        ],
        "discrepancy": {
            "heading": "Factory vs. European DC Intake Reconciliation (Display Lot DISP-P11-904)",
            "table_data": [
                ["Component Lot ID", "Assembly Line", "Factory ATE Variance", "European DC Verified Defect Rate", "Discrepancy Status"],
                ["DISP-P11-901", "Line A-1", "0.4%", "0.6%", "CONFIRMED_NOMINAL"],
                ["DISP-P11-902", "Line A-2", "0.5%", "0.7%", "CONFIRMED_NOMINAL"],
                ["DISP-P11-903", "Line B-1", "0.8%", "1.1%", "CONFIRMED_NOMINAL"],
                ["DISP-P11-904", "Line B-3", "1.2%", "9.6% (mismatch)", "FLAGGED_CRITICAL_VARIANCE"],
                ["DISP-P11-905", "Line C-1", "0.6%", "0.8%", "CONFIRMED_NOMINAL"]
            ]
        }
    },
    "excel": {
        "title": "Google Store - DHL Express & DPD European Carrier Exception Ledger",
        "kpis": [
            {"label": "Consignments Tracked", "value": "85"},
            {"label": "Customs Exception Rate", "value": "14.1%"},
            {"label": "Pending Release Orders", "value": "12"},
            {"label": "At-Risk Preorder Revenue", "value": "€48,200"}
        ],
        "headers": ["Order_Reference", "Tracking_Number", "Destination_Country", "Courier_Partner", "Manifest_Status", "Exception_Reason", "Action_Required"],
        "rows": [
            ["ORD-2026-8701", "DHL-8701-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "UN3481 Lithium battery safety paperwork discrepancy at Brussels Air Hub", "Submit amended dangerous goods declaration"],
            ["ORD-2026-8702", "DHL-8702-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "UN3481 Lithium battery safety paperwork discrepancy at Brussels Air Hub", "Submit amended dangerous goods declaration"],
            ["ORD-2026-8703", "DHL-8703-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "Pallet dimension mismatch on consolidation manifest", "Issue re-manifesting order"],
            ["ORD-2026-8704", "DPD-8704-EU", "France (FR)", "DPD Europe", "IN_TRANSIT", "Cleared Roissy hub; out for delivery today", "Normal monitoring"],
            ["ORD-2026-8706", "DHL-8706-EU", "Germany (DE)", "DHL Express", "DELIVERED", "Delivered to customer reception with signed POD", "Completed"],
            ["ORD-2026-8707", "DHL-8707-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "UN3481 Lithium battery safety paperwork discrepancy at Brussels Air Hub", "Submit amended dangerous goods declaration"],
            ["ORD-2026-8710", "DHL-8710-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "Held at Madrid Barajas sorting facility", "Priority courier clearance requested"],
            ["ORD-2026-8712", "DHL-8712-EU", "Spain (ES)", "DHL Express", "ESCALATED", "Customer reported damaged outer carton and screen defect", "Initiate RMA return and courier insurance claim"],
            ["ORD-2026-8715", "DPD-8715-EU", "France (FR)", "DPD Europe", "DELIVERED", "Delivered to parcel locker", "Completed"],
            ["ORD-2026-8720", "UPS-8720-EU", "Italy (IT)", "UPS", "IN_TRANSIT", "On vehicle for delivery in Milan", "Normal monitoring"],
            ["ORD-2026-8728", "DHL-8728-EU", "UK", "DHL Express", "DELIVERED", "Delivered with signature", "Completed"],
            ["ORD-2026-8735", "DHL-8735-EU", "Spain (ES)", "DHL Express", "CUSTOMS_HOLD", "UN3481 Lithium battery safety paperwork discrepancy at Brussels Air Hub", "Submit amended dangerous goods declaration"]
        ]
    },
    "scans": [
        {
            "title": "Google Store - B2X European Service Center Hardware Diagnostic Intake",
            "doc_no": "B2X-FRA-2026-0902-RMA",
            "date": "2026-09-02",
            "headers": ["Item", "Device Serial / IMEI", "Reported Customer Defect", "Laboratory Diagnostic Finding", "Triage Disposition"],
            "rows": [
                ["1", "IMEI-35829104882101", "Severe screen flicker below 30% brightness", "Confirmed PWM pulse instability. Hardware linked to lot DISP-P11-904.", "Warranty Replacement Approved"],
                ["2", "IMEI-35829104882144", "Lock screen green flash on ambient display", "High frequency flicker detected on optical photodiode sensor. Lot DISP-P11-904.", "Warranty Replacement Approved"],
                ["3", "IMEI-35829104882199", "Display flashing when opening Camera app", "Panel voltage drop under high peak brightness burst. Lot DISP-P11-904.", "Warranty Replacement Approved"]
            ],
            "is_discrepancy": True
        },
        {
            "title": "Google Store - CTDI Wearables Quality Assurance Certification",
            "doc_no": "CTDI-MAD-2026-0904-QA",
            "date": "2026-09-04",
            "headers": ["Item", "Device Serial Number", "Inspected Sub-system", "Test Metric", "Certification Result"],
            "rows": [
                ["1", "SN-PW5-8829104-ES", "Pixel Watch 5 Ceramic Bio-Sensor Gasket", "Hydrostatic 5ATM Pressure Seal", "Seal Failure - Moisture Ingress"],
                ["2", "SN-PW5-8810294-DE", "Pixel Watch 5 Linear Haptic Resonator", "Resonant Frequency 180Hz", "Certified Nominal Pass"],
                ["3", "SN-PBP3-991204-FR", "Pixel Buds Pro 3 Acoustic Chamber", "Noise Isolation Curve 42dB", "Certified Nominal Pass"]
            ],
            "is_discrepancy": False
        }
    ]
}

with open(os.path.join(DATA_DIR, "external_files_spec.json"), "w", encoding="utf-8") as f:
    json.dump(external_files_spec, f, indent=2)

print("✅ All synthetic data, schemas, descriptions, and external file specs generated successfully.")
