#!/usr/bin/env python3
"""
Dynamically generates the 8-step Presenter's Stage Playbook (Markdown & PDF)
using the active deployment's live URLs (Gemini Enterprise Chat URL, BigQuery
Studio table link, Google Drive proof links, and Operations Viewer URL), and
uploads the generated playbook to the deployer's Google Drive folder.
"""
import os
import sys
import json
import subprocess
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_and_upload_external_files import drive_access_token, drive_upload_file

EXT_DIR = os.path.join(BASE_DIR, "external_files")
os.makedirs(EXT_DIR, exist_ok=True)
MD_PATH = os.path.join(EXT_DIR, "GEMINI_ENTERPRISE_DEMO_SCRIPT.md")
ROOT_MD_PATH = os.path.join(BASE_DIR, "GEMINI_ENTERPRISE_DEMO_SCRIPT.md")
PDF_PATH = os.path.join(EXT_DIR, "GEMINI_ENTERPRISE_DEMO_SCRIPT.pdf")
SUMMARY_PATH = os.path.join(EXT_DIR, "drive_upload_summary.json")


def _read_file_text(path: str) -> str:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                return fh.read().strip()
    except Exception:
        pass
    return ""


def _resolve_context():
    project_id = os.environ.get("PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT") or ""
    if not project_id:
        try:
            project_id = subprocess.check_output(
                ["gcloud", "config", "get-value", "project"], stderr=subprocess.DEVNULL, text=True
            ).strip()
        except Exception:
            project_id = "YOUR_GCP_PROJECT_ID"

    dataset_id = (
        os.environ.get("DATASET_ID")
        or os.environ.get("BIGQUERY_DATASET")
        or "demo_google_store_2654"
    )

    gcp_account = os.environ.get("GCP_ACCOUNT") or ""
    if not gcp_account or gcp_account == "Unknown":
        try:
            gcp_account = subprocess.check_output(
                ["gcloud", "config", "get-value", "account"], stderr=subprocess.DEVNULL, text=True
            ).strip()
        except Exception:
            gcp_account = "your-deployed-gcp-account"

    chat_url = (
        os.environ.get("GE_DIRECT_CHAT_URL")
        or _read_file_text(os.path.join(BASE_DIR, ".ge_direct_url"))
        or f"https://console.cloud.google.com/gemini-enterprise/overview?project={project_id}"
    )

    viewer_url = (
        os.environ.get("VIEWER_URL")
        or os.environ.get("DATA_VIEWER_URL")
        or _read_file_text(os.path.join(BASE_DIR, ".viewer_url"))
        or f"https://console.cloud.google.com/run?project={project_id}"
    )

    bq_url = (
        f"https://console.cloud.google.com/bigquery?project={project_id}"
        f"&ws=!1m5!1m4!4m3!1s{project_id}!2s{dataset_id}!3shub_inventory"
    )

    gcs_bucket = os.environ.get("GCS_BUCKET_NAME") or f"{project_id}-gstore-2654-docs"
    pdf_url = f"https://storage.cloud.google.com/{gcs_bucket}/google-store_audit_report.pdf"
    xlsx_url = f"https://storage.cloud.google.com/{gcs_bucket}/google-store_external_ledger.xlsx"
    folder_id = ""
    summary_data = {}

    if os.path.exists(SUMMARY_PATH):
        try:
            with open(SUMMARY_PATH, "r", encoding="utf-8") as fh:
                summary_data = json.load(fh)
            folder_id = summary_data.get("folder_id", "")
            if summary_data.get("owner_account"):
                gcp_account = summary_data["owner_account"]
            for item in summary_data.get("uploaded_files", []):
                fname = item.get("fileName", "")
                furl = item.get("url", "")
                if fname == "google-store_audit_report.pdf" and furl.startswith("http"):
                    pdf_url = furl
                elif fname == "google-store_external_ledger.xlsx" and furl.startswith("http"):
                    xlsx_url = furl
        except Exception:
            pass

    return {
        "project_id": project_id,
        "dataset_id": dataset_id,
        "gcp_account": gcp_account,
        "chat_url": chat_url,
        "viewer_url": viewer_url,
        "bq_url": bq_url,
        "pdf_url": pdf_url,
        "xlsx_url": xlsx_url,
        "folder_id": folder_id,
        "summary_data": summary_data,
    }


ctx = _resolve_context()

# Generate Markdown Content
md_content = f"""# 🎬 Gemini Enterprise: Presenter's Stage Playbook & Run of Show
**Domain**: Google Store Hardware Launch Operations (`store.google.com`)  
**Target Hardware**: Pixel 11, Pixel 11 Pro, Pixel 11 Pro Fold, Pixel Watch 5  
**Deployed GCP Project**: `{ctx['project_id']}` (BigQuery Dataset: `{ctx['dataset_id']}`)  
**Audience**: Cross-Industry Business Executives, IT Leaders, Operations Heads & Cloud Architects  
**Format**: Live Interactive Demo with Stage Directions, Tab Switching, A2UI Click Flow & Slide Deck Generation  

---

## 🖥️ Step 0: Pre-Flight Browser Tab Setup (Stage Checklist)

Before beginning the presentation, open a **single browser window** signed in as **`{ctx['gcp_account']}`** and arrange these **5 tabs in this exact order**:

| Tab # | Name / Application | Exact URL | Stage Role |
| :---: | :--- | :--- | :--- |
| **Tab 1** | 💬 **Gemini Enterprise Chat** | [**Open Chat Session**]({ctx['chat_url']}) | **Main Stage**: Where you run all 8 prompts and interact with A2UI cards. |
| **Tab 2** | 📊 **BigQuery Studio (Schema & Data)** | [**Open `hub_inventory` in BigQuery**]({ctx['bq_url']}) | **Proof 1**: Shows governance formulas in **Schema tab** & real values (1250 vs 1680) in **Preview tab** for Prompt 2. |
| **Tab 3** | 📄 **Supplier Quality 2-Page PDF** | [**Open `google-store_audit_report.pdf`**]({ctx['pdf_url']}) | **Proof 2**: Pre-scroll to Page 2 (Section 4 Table: 9.6% vs 1.2% calibration drift for Lot DISP-P11-904) for Prompt 3. |
| **Tab 4** | 📊 **Carrier Discrepancy 85-Row Excel** | [**Open `google-store_external_ledger.xlsx`**]({ctx['xlsx_url']}) | **Proof 3**: Shows 85 tracking rows with 12 DHL customs holds (UN3481) at Brussels Air Hub for Prompt 5. |
| **Tab 5** | 🌐 **Real-Time Operations Console** | [**Open Operations Viewer**]({ctx['viewer_url']}) | **Proof 4**: Live task queue showing real-time database state transition (`PENDING_APPROVAL` ➔ `COMPLETED`) after clicking A2UI buttons. |

---

## 💡 Executive Primer: De-Jargoning the Demo

### What is an "RMA"?
**RMA** stands for **Return Merchandise Authorization**.
- **In plain English**: It is an official **customer warranty or defect return ticket**. When a customer says *"My new phone's screen flickers, I need a replacement,"* an RMA ticket tracks the return, diagnostic inspection, and replacement.
- **How to translate this to any audience**:
  - 🏦 **Banking & Financial Services**: A disputed transaction, fraud alert, or chargeback claim.
  - 🏥 **Healthcare & Pharma**: A medical equipment maintenance alert, drug recall ticket, or patient complaint.
  - 🏢 **Insurance**: A first notice of loss (FNOL) or property damage claim under review.
  - 💻 **IT / Software / SaaS**: A P1 production outage ticket, bug escalation, or SLA breach report.

### Other Quick Terms:
- **DC (Distribution Center)**: A central regional warehouse (e.g., Tilburg, Netherlands). *Every company has storage or service hubs.*
- **SLA (Service Level Agreement)**: The contractual promise on delivery time (e.g., delivered within 48 hours).
- **Cross-Source Lineage**: Connecting data stored in different formats (e.g. an Asian supplier's PDF report + a European courier's Excel file + Google Cloud BigQuery database).

---

## 🎯 Step-by-Step Choreography: Prompts, Tab Cues, Clicks & Audience Translation

```
Step 1: Overview (Tab 1)
   ↓
Step 2: Governance & Proof (Tab 1 ➔ Tab 2 Schema & Preview ➔ Tab 1)
   ↓
Step 3: Cross-Source WOW (Tab 1 ➔ Tab 3 Page 2 ➔ Tab 1)
   ↓
Step 4: Immediate Action (Tab 1 [Click A2UI] ➔ Tab 5 ➔ Tab 1)
   ↓
Step 5: Background Batch (Tab 1 [Click Sandbox] ➔ Tab 4 ➔ Tab 1)
   ↓
Step 6: 24/7 Monitoring (Tab 1 ➔ Tab 5 ➔ Tab 1)
   ↓
Step 7: Executive ROI (Tab 1 [Full Synthesis])
   ↓
Step 8: Autonomous Slide Deck Generation (Tab 1 [Download .pptx])
```

---

### 🔹 Step 1: Foundation & Data Overview
* **Stage Direction**: Start on **Tab 1 (Gemini Enterprise Chat)**.

#### 📋 Prompt to Copy-Paste:
```text
Hello! As the Google Store Operations Manager, can you give me an executive operational overview of our European launch status for the Pixel 11, Pixel 11 Pro, and Pixel Watch 5 lineup? Show me the active distribution hubs, total on-hand stock vs preorder reservations, and highlight any inventory bottlenecks across our European logistics network.
```

#### 🎬 Stage Action & A2UI Interaction:
1. Hit enter and let the agent stream the response.
2. The agent outputs a clean welcome greeting and renders a structured A2UI `MaterialTable` comparing **Tilburg**, **Dublin**, **Frankfurt**, and **Madrid**.
3. 🛑 **A2UI Click Action**: **DO NOT CLICK ANY BUTTONS YET.** Let the table remain on screen while you walk the audience through the numbers.
4. **Point to Screen**: Point to Row 1 (`NL-TILBURG-01`): On-hand stock is **1,250**, but preorder reservations are **1,680** (a **430-unit deficit** with status `CRITICAL_BACKORDER`).

#### 🎙️ What You Say to the Audience:
> *"Notice that I didn't write a SQL query, and I didn't have to submit a ticket to the Business Intelligence team and wait two weeks. I just asked in plain English. Gemini Enterprise queries our live database, formats the numbers, and gives me an instant operational snapshot. This works whether you're looking at retail inventory, bank transactions, or hospital bed capacity."*

#### 🌍 Universal Industry Translation:
- **Banking**: *"Show me today's mortgage approvals vs pending verifications across all branches."*
- **Healthcare**: *"Show me current ICU bed availability vs incoming emergency admissions across our regional clinics."*

---

### 🔹 Step 2: Knowledge Catalog Metadata Discovery (Where to See Rules & Values)
* **Stage Direction**: Start on **Tab 1**, switch to **Tab 2 (BigQuery Studio)**, then return to **Tab 1**.

#### 📋 Prompt to Copy-Paste:
```text
Before we take action on inventory levels, can you check the Knowledge Catalog metadata for the hub_inventory table? Specifically explain the business definitions and calculation rules for `safety_threshold` and `stock_status`, and confirm which status values trigger an automated replenishment alert under Google Store fulfillment standards.
```

#### 🎬 Stage Action & A2UI Interaction:
1. Hit enter. The agent explains the governance formulas and status trigger rules.
2. 🔄 **Tab Switch Cue**: **Switch to Tab 2 (BigQuery Studio)**:
   * **Where the Business Rule is Documented**: Click the **Schema** tab:
     - Field **`safety_threshold`**: Look at the **Description** column:
       > *"Minimum safety buffer stock threshold. Calculation formula: safety_threshold = (Average Daily Dispatch Volume x Replenishment Lead Days) + Safety Buffer Margin. Set between 200 and 500 units depending on hub tier."*
     - Field **`stock_status`**: Look at the **Description** column:
       > *"Operational inventory health status governed by business rule: 'CRITICAL_BACKORDER' if (on_hand_stock - reserved_preorders < 0) [triggers immediate automated replenishment alert]; 'CONSTRAINED' if (on_hand_stock - reserved_preorders <= safety_threshold); 'HEALTHY' if buffer margin is satisfied. Valid enum values: HEALTHY, CONSTRAINED, CRITICAL_BACKORDER."*
   * **Where the Real-World Data Values are Seen**: Click the **Preview** tab (right next to Schema):
     - Point to Row 1 (`NL-TILBURG-01`):
       - `on_hand_stock` = **`1250`**
       - `reserved_preorders` = **`1680`**
       - Calculation: `1250 - 1680 = -430 (< 0)` ➔ **Triggers `CRITICAL_BACKORDER`!**
       - `safety_threshold` = **`500`**
     - Point to Row 2 (`IE-DUBLIN-02`):
       - `on_hand_stock` = **`920`**
       - `reserved_preorders` = **`410`**
       - Calculation: `920 - 410 = 510 (> safety_threshold 250)` ➔ **Triggers `HEALTHY`!**
3. 🔄 **Tab Switch Cue**: **Switch back to Tab 1 (Chat)**:
   * Show that Gemini extracted both the corporate formula and the exact status triggers without writing custom code.

#### 🎙️ What You Say to the Audience:
> *"Every enterprise has its own business rules, formulas, and alert thresholds. With generic AI, the model guesses what a word means and hallucinates. Here, Gemini Enterprise reads the official corporate data definitions right from BigQuery and Dataplex. It knows the exact formula for 'safety_threshold' and why Tilburg is in critical backorder before taking any action."*

#### 🌍 Universal Industry Translation:
- **Financial Compliance**: Explaining corporate definitions of *"Affluent Client"* or *"High-Risk AML Transaction"*.
- **Insurance**: Verifying company guidelines for *"Total Loss Calculation"* in underwriting.

---

### 🔹 Step 3: Cross-Source Discovery [THE WOW MOMENT]
* **Stage Direction**: Start on **Tab 1**, switch to **Tab 3 (Google Drive 2-Page PDF)**, then return to **Tab 1**.

#### 📋 Prompt to Copy-Paste:
```text
We're seeing a spike in customer RMA warranty returns for screen flicker on the Pixel 11 Pro 256GB Obsidian in Europe. Can you cross-reference our internal `rma_defect_records` table with the external factory quality audit report (google-store_audit_report.pdf) from our Asian assembly plant? Identify which component sub-lot is causing the failure, quantify the discrepancy between factory gate testing and European service center intake, and identify affected customer orders.
```

#### 🎬 Stage Action & A2UI Interaction:
1. Hit enter. Gemini begins reading the PDF and joining it against BigQuery return tickets.
2. 🔄 **Tab Switch Cue**: **Switch to Tab 3 (Google Drive PDF)** while Gemini streams:
   * **Show the Audience**: Scroll down to **Page 2, Section 4: Factory Gate Testing vs European DC Intake Reconciliation**:
     - Point to **Row 4 (highlighted in red)**: Component Lot **`DISP-P11-904`** (Assembly Line B-3).
     - Factory ATE Variance = **`1.2%`**; European DC Verified Defect Rate = **`9.6% (Critical Mismatch)`**; Status = `FLAGGED_CRITICAL_VARIANCE`.
   * Tell the audience: *"Notice this PDF was sent from our manufacturer in Asia. It is NOT in our database—it is just an unstructured document sitting in Google Drive."*
3. 🔄 **Tab Switch Cue**: **Switch back to Tab 1 (Chat)**:
   * Show how Gemini extracted that exact `DISP-P11-904` lot number from Page 2 of the PDF, identified the **8.4% calibration drift**, and matched it directly to affected European customer orders (`ORD-2026-8701`, `ORD-2026-8712`, etc.) in BigQuery!

#### 🎙️ What You Say to the Audience:
> *"This is the moment that transforms how business gets done. We have an external PDF sent by a hardware manufacturer in Asia sitting in Google Drive. Watch how Gemini reads that PDF, extracts the factory calibration data, and joins it directly with our internal customer repair records in BigQuery. In most enterprises, connecting an external vendor report to customer records takes three meetings and two weeks of manual spreadsheets. Gemini did it in seconds."*

#### 🌍 Universal Industry Translation:
- **Banking**: Cross-referencing an external regulator PDF sanction notice with internal customer bank accounts.
- **Healthcare / Pharma**: Matching a medical device manufacturer recall notice in PDF with internal surgical patient logs.

---

### 🔹 Step 4: Multi-Step Immediate Workflow [ACTION & HITL]
* **Stage Direction**: Start on **Tab 1**, click the A2UI button, switch to **Tab 5 (Operations Console)**, then return to **Tab 1**.

#### 📋 Prompt to Copy-Paste:
```text
Our Tilburg Central DC (NL-TILBURG-01) is facing a critical 430-unit deficit for the Pixel 11 Pro 256GB Obsidian, putting European preorder delivery SLAs at severe risk. Scan the rest of our European logistics network for available buffer stock, propose an immediate inter-hub stock rebalancing transfer, and prepare the authorization request.
```

#### 🎬 Stage Action & A2UI Interaction:
1. Hit enter. Gemini scans all European hubs, discovers that **Dublin (`IE-DUBLIN-02`) has a 450-unit surplus**, and renders an interactive **A2UI MaterialCard** titled *"Emergency Inter-Hub Stock Transfer Authorization"*.
2. 🖱️ **HERO CLICK ACTION**: **Click the blue `[Approve Stock Transfer]` button on the A2UI Card!**
   * The agent executes real BigQuery DML (`UPDATE`) and updates Firestore: *"Stock transfer authorized. Dispatching 450 units of Pixel 11 Pro Obsidian from Dublin to Tilburg via Express Logistics."*
3. 🔄 **Tab Switch Cue**: **Switch immediately to Tab 5 (Real-Time Operations Console)**:
   * Show the audience the task queue: Point to **`task-launch-backorder-01`**.
   * **Point to Screen**: Show that the status has live-updated to **`COMPLETED`** with an unalterable audit log entry!
4. 🔄 **Tab Switch Cue**: **Switch back to Tab 1 (Chat)**.

*(Side Note for Audience Q&A: If someone asks "What if I don't want to approve?", explain that the card also supports rejection or custom quantity adjustments, keeping humans firmly in the driver's seat).*

#### 🎙️ What You Say to the Audience:
> *"Insight without action is useless. Instead of just giving text advice, Gemini scans our European network, finds 450 extra phones in Dublin, and generates an interactive, clickable Approval Card right in the chat. When I click 'Approve', it writes the transfer directly to our production systems. The human stays in full control, but the manual friction is gone."*

#### 🌍 Universal Industry Translation:
- **Insurance**: Generating a one-click claim settlement payout approval card.
- **Finance**: A one-click interactive widget to authorize an emergency treasury wire transfer.

---

### 🔹 Step 5: Large-Scope Batch Execution [CLOUD SANDBOX]
* **Stage Direction**: Start on **Tab 1**, click the Sandbox button, switch to **Tab 4 (Excel Ledger)**, then return to **Tab 1**.

#### 📋 Prompt to Copy-Paste:
```text
DHL Express and DPD Europe reported multiple transit exceptions across our preorder consignments. I need you to perform a full reconciliation of all delayed customer orders against the 85-row carrier discrepancy ledger (google-store_external_ledger.xlsx), resolve customs documentation holds at Brussels Air Hub, and calculate our contractual SLA clawback penalties across all delayed shipments.
```

#### 🎬 Stage Action & A2UI Interaction:
1. Hit enter. Gemini analyzes the task scope, recognizes that this involves multi-row calculation over an 85-row spreadsheet, and presents an **Execution Mode Dialog Card** with two buttons:
   * `[Run in Background (Sandbox)]` (Recommended)
   * `[Run Immediately (Sync)]`
2. 🖱️ **HERO CLICK ACTION**: **Click `[Run in Background (Sandbox)]`!**
   * The agent confirms: *"Task delegated to autonomous Cloud Sandbox. Executing in background."*
3. 🔄 **Tab Switch Cue**: **Switch to Tab 4 (Google Drive Excel Ledger)**:
   * **Show the Audience**: 
     - Point to the KPI banner at the top: `Total Consignments Tracked: 85`, `Pending Customs Release: 12`.
     - Point to Rows 7 through 18 (highlighted in light red): DHL Express shipments marked `CUSTOMS_HOLD` due to `UN3481 Lithium battery safety paperwork discrepancy at Brussels Air Hub`.
4. 🔄 **Tab Switch Cue**: **Switch back to Tab 1 (Chat)**:
   * Show that Gemini has resolved the holds, generated the amended paperwork declaration, and calculated the exact **€12,450 contractual courier penalty clawback**!

#### 🎙️ What You Say to the Audience:
> *"What happens when you ask traditional AI to reconcile an 85-row spreadsheet against complex customs rules? It crashes or times out. Gemini Enterprise recognizes that this is heavy data crunching. It delegates the work to a secure Cloud Sandbox, writing and running Python code in the background while keeping your chat responsive."*

#### 🌍 Universal Industry Translation:
- **Finance & Accounting**: Auditing 50,000 monthly employee expense receipts against tax compliance rules.
- **Cybersecurity**: Batch analysis of thousands of server firewall logs during an incident.

---

### 🔹 Step 6: Scheduled Automated Monitoring [PROACTIVE AI]
* **Stage Direction**: Start on **Tab 1**, then switch to **Tab 5 (Operations Console)**, then return to **Tab 1**.

#### 📋 Prompt to Copy-Paste:
```text
Set up an automated daily monitoring check every morning at 08:00 UTC. The agent must inspect inventory levels across all European hubs, check for any newly created CRITICAL severity RMA records (such as Pixel Watch 5 ceramic seal ingress), and register an escalation task in Firestore if safety thresholds are breached.
```

#### 🎬 Stage Action & A2UI Interaction:
1. Hit enter. Gemini confirms the registration of a recurring automated rule: `0 8 * * *` (Daily at 08:00 UTC) with task ID `task-watch-seal-audit-04`.
2. 🔄 **Tab Switch Cue**: **Switch to Tab 5 (Operations Console)**:
   * Point to the active monitoring tasks queue and show that the autonomous rule is permanently registered.
3. 🔄 **Tab Switch Cue**: **Switch back to Tab 1 (Chat)**.

#### 🎙️ What You Say to the Audience:
> *"Most AI today is purely reactive—it does nothing until a human types a prompt. Here, we register a proactive autonomous rule. Every morning at 08:00 UTC, the agent wakes up, audits inventory, scans for critical defects, and alerts the team only if action is needed. We have shifted from human-driven prompting to autonomous continuous operations."*

#### 🌍 Universal Industry Translation:
- **Banking Fraud**: Automated nightly sweeps of high-velocity wire transactions above compliance limits.
- **Retail**: Automated daily monitoring of out-of-stock items across 500 physical store locations.

---

### 🔹 Step 7: Strategic Automation & Quantified Outcomes [EXECUTIVE ROI]
* **Stage Direction**: Stay on **Tab 1 (Gemini Enterprise Chat)**.

#### 📋 Prompt to Copy-Paste:
```text
Provide an executive summary of the entire Pixel 11 and Watch 5 launch triage operation. Synthesize our actions across Fulfillment, Quality Assurance, and Logistics: summarize the units rebalanced, customs holds resolved, defective display lots quarantined, and goodwill credits issued. Quantify the final impact on customer on-time delivery rates and preorder lead time reduction.
```

#### 🎬 Stage Action & A2UI Interaction:
1. Hit enter. Gemini aggregates data across all previous turns and renders a comprehensive executive summary card with an interactive **VegaChart**.
2. 🛑 **A2UI Click Action**: DO NOT click; let the audience absorb the final ROI metrics.
3. **Point to Screen**: Point out the **3 core executive ROI numbers**:
   * 📉 **Preorder Delivery Lead Time**: Reduced from **7.2 days to 1.8 days** (75% faster).
   * 🎯 **On-Time Delivery SLA Preservation**: Maintained at **98.4%**.
   * 💰 **Unlocked Inventory**: **€48,200** in delayed shipments released from customs holds.
   * 🛡️ **Defect Containment**: Quarantined sub-lot `DISP-P11-904` before impacting general retail sales.

#### 🎙️ What You Say to the Audience:
> *"When the CEO or Board asks 'What was the ROI of this AI investment?', Gemini synthesizes data across all three departments—Logistics, Quality Engineering, and Finance. It proves the ROI: lead times dropped from 7.2 days to 1.8 days, 98.4% of customer preorders were saved from cancellation, and every single decision has an unalterable audit log."*

---

### 🔹 Step 8: Executive Deliverable — Autonomous Slide Deck Generation (.pptx) [GRAND FINALE]
* **Stage Direction**: Stay on **Tab 1 (Gemini Enterprise Chat)**.

#### 📋 Prompt to Copy-Paste:
```text
Can you generate an executive slide deck summarizing our Pixel 11 and Watch 5 launch recovery, showing the inventory rebalancing and SLA preservation metrics? Build the presentation and provide the download link.
```

#### 🎬 Stage Action & A2UI Interaction:
1. Hit enter. Gemini delegates the task to the **Agent Engine Cloud Sandbox** (`delegate_autonomous_task`).
2. Inside the sandbox, the autonomous worker uses `python-pptx` to programmatically build an authentic **16:9 widescreen presentation deck** with:
   * Title slide & Executive Summary.
   * Hub inventory rebalancing breakdown table.
   * Defective display quarantine timeline & customer goodwill recovery.
   * Quantified business ROI summary slide with speaker notes.
3. 🖱️ **HERO ACTION**: Click the generated **download link** in the chat to download the `.pptx` file directly to your laptop, or open it to show the audience the formatted slides!

#### 🎙️ What You Say to the Audience:
> *"Notice that I don't have to copy-paste numbers from the chat into PowerPoint. Gemini Enterprise's cloud sandbox writes and runs Python code in the background, generates a complete 16:9 board-level presentation deck with charts and speaker notes, and gives me the download link directly in the conversation. It takes you from data analysis to a board-ready deliverable in seconds."*

#### 🌍 Universal Industry Translation:
- **Consulting / Strategy**: Instantly converting operational analysis into client presentation decks.
- **Financial Services**: Auto-generating monthly investment committee slides or portfolio reviews.
- **Healthcare**: Auto-generating board reports on clinical trial progress or hospital operational efficiency.

---

## 🎯 3 Golden Takeaways to Close Your Presentation

1. **Enterprise Security & Data Privacy**: Runs 100% inside your private Google Cloud perimeter. Your corporate data and customer records are never used to train public foundation models.
2. **Breaks Down Silos**: Natively connects unstructured documents (PDFs, Excel, scanned notes) with structured SQL databases.
3. **From Chat to Action**: Goes beyond answering questions by generating interactive UI approval cards, executing background batch jobs, building real deliverables (.pptx slides), and enforcing human oversight every step of the way.

---

## 🔄 Fast Demo Reset (10 Seconds)
To reset the BigQuery inventory tables and Firestore approval queue back to their original pre-demo crisis state before your next presentation:
```bash
bash scripts/reset_demo_state.sh
```
"""

# Write updated Markdown in both ./external_files/ and repo root
for target_md in (MD_PATH, ROOT_MD_PATH):
    with open(target_md, "w", encoding="utf-8") as f:
        f.write(md_content)
print(f"  ✅ Markdown playbook generated: {ROOT_MD_PATH}")

# Generate PDF with ReportLab
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors

    doc = SimpleDocTemplate(PDF_PATH, pagesize=letter, rightMargin=32, leftMargin=32, topMargin=32, bottomMargin=32)
    styles = getSampleStyleSheet()

    t_style = ParagraphStyle('TStyle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#1a73e8'), spaceAfter=8)
    h1_style = ParagraphStyle('H1Style', parent=styles['Heading2'], fontSize=11.5, leading=15, textColor=colors.HexColor('#0f172a'), spaceBefore=8, spaceAfter=3, keepWithNext=True)
    h2_style = ParagraphStyle('H2Style', parent=styles['Heading3'], fontSize=9.5, leading=12, textColor=colors.HexColor('#0284c7'), spaceBefore=5, spaceAfter=2, keepWithNext=True)
    body_style = ParagraphStyle('BStyle', parent=styles['Normal'], fontSize=7.5, leading=10.5, textColor=colors.HexColor('#334155'), spaceAfter=3)
    stage_style = ParagraphStyle('StageStyle', parent=styles['Normal'], fontSize=7.5, leading=10.5, textColor=colors.HexColor('#7c3aed'), backColor=colors.HexColor('#f5f3ff'), borderPadding=4, spaceAfter=4)
    quote_style = ParagraphStyle('QStyle', parent=styles['Normal'], fontSize=7.5, leading=10.5, textColor=colors.HexColor('#1e293b'), backColor=colors.HexColor('#f1f5f9'), borderPadding=4, spaceAfter=4)
    prompt_style = ParagraphStyle('PStyle', parent=styles['Normal'], fontName='Courier', fontSize=6.8, leading=8.8, textColor=colors.HexColor('#0f172a'), backColor=colors.HexColor('#e2e8f0'), borderPadding=4, spaceAfter=4)

    story = []
    story.append(Paragraph("🎬 Gemini Enterprise: Presenter's Stage Playbook & Run of Show", t_style))
    story.append(Paragraph(f"<b>Google Store Consumer Hardware Launch Operations | Project: {ctx['project_id']}</b>", h2_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1a73e8'), spaceAfter=8))

    # Step 0 Table
    story.append(Paragraph("Step 0: Pre-Flight Browser Tab Setup (Stage Checklist)", h1_style))
    story.append(Paragraph(f"Arrange these 5 tabs in a single browser window signed in as <b>{ctx['gcp_account']}</b> before presenting:", body_style))

    link_style = ParagraphStyle('LinkStyle', parent=body_style, fontSize=7, leading=9.5, textColor=colors.HexColor('#1a73e8'))
    tab_data = [
        ["Tab #", "Application / Document", "Stage Role & Clickable Link"],
        ["Tab 1", "Gemini Enterprise Chat", Paragraph(f"<b>Main Stage:</b> Run all 8 prompts & click A2UI cards (<a href='{ctx['chat_url']}'>Open Chat</a>)", body_style)],
        ["Tab 2", "BigQuery Studio (hub_inventory)", Paragraph(f"<b>Proof 1:</b> Schema formulas & Preview values (<a href='{ctx['bq_url']}'>Open BigQuery</a>)", body_style)],
        ["Tab 3", "Supplier Quality 2-Page PDF", Paragraph(f"<b>Proof 2:</b> Page 2 Section 4 Table: Lot DISP-P11-904 (<a href='{ctx['pdf_url']}'>Open 2-Page PDF</a>)", body_style)],
        ["Tab 4", "Carrier Discrepancy 85-Row Excel", Paragraph(f"<b>Proof 3:</b> 85 rows with 12 DHL holds at Brussels (<a href='{ctx['xlsx_url']}'>Open 85-Row Excel</a>)", body_style)],
        ["Tab 5", "Real-Time Operations Console", Paragraph(f"<b>Proof 4:</b> Live task queue transition (<a href='{ctx['viewer_url']}'>Open Operations Viewer</a>)", body_style)],
    ]
    t = Table(tab_data, colWidths=[40, 150, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t)
    story.append(Spacer(1, 4))

    # Executive Primer
    story.append(Paragraph("Executive Primer: De-Jargoning Key Terms", h1_style))
    story.append(Paragraph("<b>What is an RMA?</b> Return Merchandise Authorization = official <b>customer warranty return ticket</b>. When a customer returns a broken device, an RMA tracks diagnostic inspection and replacement dispatch. <i>Universal translations:</i> Banking (disputed fraud claim); Healthcare (equipment recall / adverse event); Insurance (accident claim / FNOL); IT/SaaS (P1 production outage ticket).", body_style))

    # 8 Prompts
    prompts_flow = [
        ("Step 1: Foundation & Data Overview (Tab 1)",
         "Hello! As the Google Store Operations Manager, can you give me an executive operational overview of our European launch status for the Pixel 11, Pixel 11 Pro, and Pixel Watch 5 lineup? Show me the active distribution hubs, total on-hand stock vs preorder reservations, and highlight any inventory bottlenecks across our European logistics network.",
         "Start on Tab 1. Watch Gemini render the hub_inventory table. DO NOT click buttons yet. Point to Row 1: Tilburg has 1,250 stock vs 1,680 preorders (deficit of 430 units, CRITICAL_BACKORDER).",
         "Say to Audience: 'Notice I didn't write SQL or wait two weeks for a BI dashboard. I just asked in plain English. Gemini Enterprise queries our live database and gives me an instant operational snapshot.'",
         "Universal Translation: Banking: 'Show me today's mortgage approvals vs pending verifications across all branches.'"),

        ("Step 2: Knowledge Catalog Metadata Discovery (Tab 1 -> Tab 2 Schema & Preview -> Tab 1)",
         "Before we take action on inventory levels, can you check the Knowledge Catalog metadata for the hub_inventory table? Specifically explain the business definitions and calculation rules for `safety_threshold` and `stock_status`, and confirm which status values trigger an automated replenishment alert under Google Store fulfillment standards.",
         "CUE: Switch to Tab 2 (BigQuery Studio). (1) In Schema tab, show safety_threshold formula: '(Daily Demand x Lead Days) + Margin' & stock_status alert trigger ('CRITICAL_BACKORDER if on_hand - reserved < 0'). (2) Click Preview tab: point to Tilburg (1250 on-hand, 1680 reserved -> -430 deficit < 0 -> CRITICAL_BACKORDER). Switch back to Tab 1.",
         "Say to Audience: 'Every enterprise has its own business rules. Generic AI guesses; Gemini Enterprise consults corporate schema descriptions in BigQuery, understanding exact formulas and why Tilburg is in backorder before taking action.'",
         "Universal Translation: Financial Compliance: Explaining corporate definitions of 'Affluent Client' or 'High Risk AML'."),

        ("Step 3: Cross-Source Discovery [THE WOW MOMENT] (Tab 1 -> Tab 3 Page 2 -> Tab 1)",
         "We're seeing a spike in customer RMA warranty returns for screen flicker on the Pixel 11 Pro 256GB Obsidian in Europe. Can you cross-reference our internal `rma_defect_records` table with the external factory quality audit report (google-store_audit_report.pdf) from our Asian assembly plant? Identify which component sub-lot is causing the failure, quantify the discrepancy between factory gate testing and European service center intake, and identify affected customer orders.",
         "CUE: Switch to Tab 3 (PDF). Point to Page 2, Section 4 Table: Lot DISP-P11-904 in red showing 9.6% vs 1.2%. Mention this is a raw PDF on Drive, NOT in the database. Switch back to Tab 1: Show Gemini matching lot DISP-P11-904 to customer order IDs in BigQuery!",
         "Say to Audience: 'In most companies, connecting an external vendor PDF to customer complaint tickets takes three meetings and two weeks of manual spreadsheets. Gemini did it in 5 seconds.'",
         "Universal Translation: Healthcare/Pharma: Matching a medical device manufacturer recall PDF with internal surgical logs."),

        ("Step 4: Multi-Step Immediate Workflow [ACTION & HITL] (Tab 1 [Click] -> Tab 5 -> Tab 1)",
         "Our Tilburg Central DC (NL-TILBURG-01) is facing a critical 430-unit deficit for the Pixel 11 Pro 256GB Obsidian, putting European preorder delivery SLAs at severe risk. Scan the rest of our European logistics network for available buffer stock, propose an immediate inter-hub stock rebalancing transfer, and prepare the authorization request.",
         "CLICK ACTION: Click the blue [Approve Stock Transfer] button on the A2UI Card! Then CUE: Switch to Tab 5 (Operations Console): Point to task-launch-backorder-01 turning COMPLETED live! Switch back to Tab 1.",
         "Say to Audience: 'Insight without action is useless. Gemini builds an approval button. When I click Approve, it writes directly to our production systems. The human stays in control, but manual friction is gone.'",
         "Universal Translation: Insurance: Generating a one-click claim settlement payout approval card."),

        ("Step 5: Large-Scope Batch Execution [CLOUD SANDBOX] (Tab 1 [Click] -> Tab 4 -> Tab 1)",
         "DHL Express and DPD Europe reported multiple transit exceptions across our preorder consignments. I need you to perform a full reconciliation of all delayed customer orders against the 85-row carrier discrepancy ledger (google-store_external_ledger.xlsx), resolve customs documentation holds at Brussels Air Hub, and calculate our contractual SLA clawback penalties across all delayed shipments.",
         "CLICK ACTION: On Execution Mode Dialog, click [Run in Background (Sandbox)]! CUE: Switch to Tab 4 (Excel Ledger): Show 85 tracking rows, with Rows 7-18 showing DHL CUSTOMS_HOLD (UN3481). Switch back to Tab 1: Show €12,450 clawback calculated in background.",
         "Say to Audience: 'Generic chatbots crash on massive spreadsheets. Gemini Enterprise delegates heavy lifting to a secure Cloud Sandbox, running Python code in the background while keeping your chat responsive.'",
         "Universal Translation: Finance: Auditing 50,000 monthly employee expense receipts against tax compliance policies."),

        ("Step 6: Scheduled Automated Monitoring [PROACTIVE AI] (Tab 1 -> Tab 5 -> Tab 1)",
         "Set up an automated daily monitoring check every morning at 08:00 UTC. The agent must inspect inventory levels across all European hubs, check for any newly created CRITICAL severity RMA records (such as Pixel Watch 5 ceramic seal ingress), and register an escalation task in Firestore if safety thresholds are breached.",
         "CUE: Switch to Tab 5 (Operations Console): Show the active Pub/Sub cron registration (0 8 * * *). Switch back to Tab 1.",
         "Say to Audience: 'Most AI is purely reactive. Here, we register a proactive autonomous rule. Every morning at 8 AM, the agent audits inventory and defect logs, alerting the team only if a threshold is breached.'",
         "Universal Translation: Banking Fraud: Automated nightly sweeps of high-velocity wire transactions above threshold."),

        ("Step 7: Strategic Automation & Quantified Outcomes [EXECUTIVE ROI] (Tab 1)",
         "Provide an executive summary of the entire Pixel 11 and Watch 5 launch triage operation. Synthesize our actions across Fulfillment, Quality Assurance, and Logistics: summarize the units rebalanced, customs holds resolved, defective display lots quarantined, and goodwill credits issued. Quantify the final impact on customer on-time delivery rates and preorder lead time reduction.",
         "DO NOT CLICK. Point to the 3 ROI numbers on screen: (1) Lead time reduced 7.2 to 1.8 days (75% faster); (2) 98.4% preorder SLA preserved; (3) €48,200 in delayed inventory unlocked from customs.",
         "Say to Audience: 'When leadership asks What was the ROI of this AI investment?, Gemini synthesizes results across Logistics, Quality, and Finance, proving tangible business impact with an unalterable audit trail.'",
         "Universal Translation: Board-ready executive summaries showing hours saved, revenue protected, and compliance logs."),

        ("Step 8: Autonomous Slide Deck Generation (.pptx) [GRAND FINALE] (Tab 1)",
         "Can you generate an executive slide deck summarizing our Pixel 11 and Watch 5 launch recovery, showing the inventory rebalancing and SLA preservation metrics? Build the presentation and provide the download link.",
         "Stay on Tab 1. Watch Gemini invoke the Cloud Sandbox (delegate_autonomous_task) to build an authentic 16:9 widescreen .pptx presentation. Click the delivered download link in chat to download the deck!",
         "Say to Audience: 'Notice I don't copy-paste numbers from chat into PowerPoint. Gemini's cloud sandbox writes and runs Python code in the background, generates a complete 16:9 board-level deck with charts and speaker notes, and gives me the download link directly in the conversation.'",
         "Universal Translation: Consulting & Strategy: Instantly converting complex multi-source operational analysis into client presentation decks.")
    ]

    for title, prompt, choreo, say_text, translation in prompts_flow:
        story.append(Paragraph(title, h1_style))
        story.append(Paragraph("<b>Prompt to Copy-Paste:</b>", body_style))
        story.append(Paragraph(prompt, prompt_style))
        story.append(Paragraph(f"<b>🎬 Stage Directions & Click Flow:</b> {choreo}", stage_style))
        story.append(Paragraph(f"<b>🎙️ What You Say:</b> {say_text}", quote_style))
        story.append(Paragraph(f"<b>🌍 Universal Industry Translation:</b> {translation}", body_style))
        story.append(Spacer(1, 2))

    doc.build(story)
    print(f"  ✅ PDF playbook generated: {PDF_PATH}")
except Exception as e:
    print(f"  ⚠️ PDF playbook generation error: {e}")

# Upload Markdown and PDF to Google Drive if a folder exists
folder_id = ctx["folder_id"]
if folder_id and os.environ.get("SKIP_DRIVE_UPLOAD", "").strip().lower() not in ("1", "true", "yes"):
    token = drive_access_token()
    if token:
        uploaded_list = ctx["summary_data"].get("uploaded_files", [])
        for fpath in (PDF_PATH, MD_PATH):
            if not os.path.exists(fpath):
                continue
            fname = os.path.basename(fpath)
            fid, err = drive_upload_file(token, fpath, folder_id)
            if fid:
                furl = f"https://drive.google.com/file/d/{fid}/view"
                print(f"  ✅ Uploaded {fname} to Drive: {furl}")
                # Update or append in drive_upload_summary.json
                updated = False
                for entry in uploaded_list:
                    if entry.get("fileName") == fname:
                        entry["fileId"] = fid
                        entry["url"] = furl
                        entry["localPath"] = fpath
                        updated = True
                        break
                if not updated:
                    uploaded_list.append({
                        "fileName": fname,
                        "fileId": fid,
                        "url": furl,
                        "localPath": fpath,
                    })
        if ctx["summary_data"]:
            ctx["summary_data"]["uploaded_files"] = uploaded_list
            with open(SUMMARY_PATH, "w", encoding="utf-8") as fh:
                json.dump(ctx["summary_data"], fh, indent=2, ensure_ascii=False)
