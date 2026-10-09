### `customer_orders` - Individual customer hardware purchase orders, shipping destinations, courier tracking, and dispatch statuses on Google Store Europe.
Rows: 119. Coverage: `order_placed_at` 2026-08-26 -> 2026-09-17; `promised_delivery_date` 2026-08-29 -> 2026-09-22
  - `order_id` STRING - Unique Google Store customer order number (PK, e.g. ORD-2026-8701)
  - `customer_id` STRING - Anonymized customer account identifier
  - `sku_id` STRING - Ordered hardware model SKU (FK to products_catalog.sku_id)
  - `order_placed_at` TIMESTAMP - Exact order placement timestamp
  - `promised_delivery_date` DATE - Customer SLA promised delivery date
  - `fulfillment_hub` STRING - Fulfillment center assigned to dispatch order (FK to hub_inventory.hub_code) | values: DE-FRANKFURT-01, ES-MADRID-01, IE-DUBLIN-02, NL-TILBURG-01
  - `destination_country` STRING - Destination country ISO code (ES, FR, DE, IT, UK) | values: DE, ES, FR, IT, UK
  - `shipping_city` STRING - Destination shipping metropolitan city
  - `carrier_partner` STRING - Assigned parcel logistics courier (DHL Express, DPD Europe, UPS) | values: DHL Express, DPD Europe, UPS
  - `tracking_number` STRING - Courier parcel tracking reference code
  - `order_status` STRING - Order fulfillment state (DELIVERED, SHIPPED, ALLOCATED, TRANSIT_DELAYED, PENDING_INSPECTION, ESCALATED_DISPUTE) | values: ALLOCATED, DELIVERED, ESCALATED_DISPUTE, PENDING_INSPECTION, SHIPPED, TRANSIT_DELAYED
  - `total_paid_eur` FLOAT - Final customer transaction value in Euro (€)
  - `priority_flag` STRING - Customer service priority classification (STANDARD, HIGH_PRIORITY_VIP) | values: HIGH_PRIORITY_VIP, STANDARD

### `hub_inventory` - Fulfillment warehouse stock and launch preorder reservation levels across European distribution centers for Google Store.
Rows: 88. Coverage: no date column
  - `inventory_id` STRING - Inventory ledger identifier (PK, e.g. INV-1001)
  - `hub_code` STRING - Fulfillment center facility code (NL-TILBURG-01, IE-DUBLIN-02, DE-FRANKFURT-01, ES-MADRID-01) | values: DE-FRANKFURT-01, ES-MADRID-01, IE-DUBLIN-02, NL-TILBURG-01
  - `hub_name` STRING - Full logistics hub facility name
  - `country_code` STRING - Facility country ISO code (NL, IE, DE, ES) | values: DE, ES, IE, NL
  - `sku_id` STRING - Google Store hardware product SKU (FK to products_catalog.sku_id)
  - `on_hand_stock` INTEGER - Physical unit inventory count present in warehouse shelves
  - `reserved_preorders` INTEGER - Units allocated to pending customer preorders awaiting dispatch
  - `safety_threshold` INTEGER - Minimum safety buffer stock threshold. Calculation formula: safety_threshold = (Average Daily Dispatch Volume x Replenishment Lead Days) + Safety Buffer Margin. Set between 200...
  - `replenishment_lead_days` INTEGER - Estimated transit days required for stock replenishment from manufacturing source
  - `stock_status` STRING - Operational inventory health status governed by business rule: 'CRITICAL_BACKORDER' if (on_hand_stock - reserved_preorders < 0) [triggers immediate automated replenishment alert... | values: CONSTRAINED, CRITICAL_BACKORDER, HEALTHY

### `products_catalog` - Master catalog of Google hardware devices, smartphones, smartwatches, smart home, and official accessories sold on store.google.com with retail MSRP in Euro.
Rows: 22. Coverage: no date column
  - `sku_id` STRING - Unique Google hardware product SKU code (PK, e.g. SKU-PX11P-256-OBS)
  - `product_name` STRING - Commercial product model name (e.g. Pixel 11 Pro 256GB Obsidian)
  - `product_family` STRING - Hardware category (Pixel Smartphone, Pixel Watch, Audio, Smart Home, Accessories) | values: Accessories, Audio, Pixel Smartphone, Pixel Watch, Smart Home
  - `color_finish` STRING - Factory colorway and finish (Obsidian, Porcelain, Hazel, Lemongrass)
  - `storage_capacity` STRING - Internal storage capacity or size (128GB, 256GB, 512GB, 1TB, 41mm, 45mm)
  - `msrp_eur` FLOAT - Official retail launch price in Euro (EUR €)
  - `warranty_months` INTEGER - Standard manufacturer hardware warranty duration in months
  - `launch_tier` STRING - Product launch priority tier (Tier 1 Priority, General Availability) | values: General Availability, Tier 1 Priority

### `rma_defect_records` - Warranty return authorizations, hardware defect diagnostics, and service center triage logs for Google Store devices.
Rows: 35. Coverage: `incident_date` 2026-09-02 -> 2026-09-18
  - `rma_id` STRING - Return Merchandise Authorization identifier (PK, e.g. RMA-2026-0401)
  - `order_id` STRING - Associated Google Store customer order (FK to customer_orders.order_id)
  - `sku_id` STRING - Hardware device SKU undergoing RMA evaluation (FK to products_catalog.sku_id)
  - `serial_number` STRING - Device IMEI number or hardware serial code
  - `incident_date` TIMESTAMP - Date and time when warranty return incident was logged
  - `defect_category` STRING - Diagnostic root defect category (OLED_MICRO_FLICKER, BATTERY_CALIBRATION_DRIFT, CERAMIC_SEAL_BREACH, HAPTIC_FEEDBACK_VARIANCE)
  - `defect_severity` STRING - Defect classification impact severity (LOW, MEDIUM, HIGH, CRITICAL) | values: CRITICAL, HIGH, LOW, MEDIUM
  - `technician_diagnostic_summary` STRING - Authorized repair technician diagnostic findings and observations
  - `triage_status` STRING - Current RMA resolution stage (PENDING_TRIAGE, VERIFIED_HARDWARE_FAULT, REPLACEMENT_DISPATCHED, REFUND_CREDITED, REJECTED_CUSTOMER_DAMAGE) | values: PENDING_TRIAGE, REFUND_CREDITED, REPLACEMENT_DISPATCHED, VERIFIED_HARDWARE_FAULT
  - `assigned_repair_center` STRING - Certified European repair center handling inspection (B2X Frankfurt, CTDI Madrid, CTDI Paris) | values: B2X European Repair Center (Frankfurt), CTDI Logistics & Repair (Madrid), CTDI Logistics & Repair (Paris)
  - `refund_credit_eur` FLOAT - Processed financial compensation or Google Store goodwill voucher in Euro (€)
  - `customer_sentiment` STRING - Assessed customer emotional sentiment during ticket escalation (SATISFIED, NEUTRAL, ANXIOUS, FRUSTRATED) | values: ANXIOUS, DISSATISFIED, FRUSTRATED, NEUTRAL, SATISFIED
