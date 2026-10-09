# Google Store Hardware Operations — Gemini Enterprise Live Demo (`store.google.com`)

An end-to-end, multi-agent **Gemini Enterprise** executive demo for **Google Store European Hardware Operations & Supply Chain Resilience** (Pixel 11 Pro & Pixel Watch 4 launch wave).

With a **single command (`bash setup_and_deploy.sh`)**, this repository provisions the entire demo stack inside **your own GCP project**, uploads the external proof documents to **your own Google Drive**, registers the agent in **your Gemini Enterprise engine**, and generates a **personalized Director's Cut Presenter Playbook** (`GEMINI_ENTERPRISE_DEMO_SCRIPT.pdf` and `.md`) containing your live clickable URLs.

---

## 🌟 What This Demo Showcases (8-Step Narrative Arc)

| Step | Capability | What Happens Live |
| :--- | :--- | :--- |
| **Prompt 1** | **BigQuery SQL Analytics + Executive KPI Cards** | Queries `customer_orders`, `hub_inventory`, `products_catalog`, and `rma_defect_records` to pinpoint **4 `CRITICAL_BACKORDER` rows** (-610 net deficit; **-190 units** of Pixel 11 Pro 256GB Obsidian at **Tilburg NL-TILBURG-01**) and **€7,780** in OLED micro-flicker RMA credits across **14 cases**. |
| **Prompt 2** | **Knowledge Catalog & Data Governance** | Queries Data Catalog / Knowledge Catalog column descriptions on `hub_inventory` to retrieve the official formula for `safety_threshold` (`(Avg Daily Dispatch Volume × Replenishment Lead Days) + Safety Buffer Margin`) and the 3-tier business rules for `stock_status` without scanning table rows. |
| **Prompt 3** | **Cross-Source RAG (BigQuery + 2-Page PDF + 85-Row Excel)** | Cross-references live BigQuery tables against the **2-page QA Audit PDF** (`google-store_audit_report.pdf`, Page 2 Table 2: **8.4% OLED calibration drift** on Lot `#LOT-2026-PX11P-09B`) and the **85-row Carrier Discrepancy Excel Ledger** (`google-store_external_ledger.xlsx`: **€42,500** SLA penalty exposure). |
| **Prompt 4** | **Multimodal Vision OCR & Fraud/Tampering Detection** | Compares two scanned warehouse intake slips (`google-store_simulated_order_task1.jpg` vs `google-store_simulated_order_task2_discrepancy.jpg`), catching a **-150 unit short-shipment** on `REF-0101`, an unauthorized SKU substitution (`REF-9901`), and a **-240 unit discrepancy** on `REF-0309`. |
| **Prompt 5** | **Synchronous Multi-Database Write-Back (Firestore + BigQuery DML)** | Approves and executes an emergency **+350 unit air-freight reallocation** to Tilburg (`NL-TILBURG-01`), updating Firestore (`TASK-101` -> `COMPLETED`) and running a live BigQuery `UPDATE` (`on_hand_stock` **420 -> 770**, `stock_status` -> **`HEALTHY`**). |
| **Prompt 6** | **Asynchronous Long-Running Task + Real-Time Operations Console** | Dispatches a heavy 85-row carrier customs & SLA clawback reconciliation to a background worker (`TASK-102`), streaming live progress (`0% -> 25% -> 60% -> 85% -> 100%`) in the **Operations Console UI** while keeping the chat responsive. |
| **Prompt 7** | **Autonomous Python Sandbox Execution (Agent Engine Code Interpreter)** | Spins up an isolated **Agent Engine Code Execution Sandbox** to run a **10,000-trial Monte Carlo simulation** (`numpy`/`pandas`) calculating exact safety stock targets for the **99.5% on-time delivery SLA**. |
| **Prompt 8** | **Executive Board Deck & Interactive HTML Briefing (`SkillToolset`)** | Packages all session findings into an interactive **C-Suite Executive HTML Briefing** (with Chart.js visualizations and CSV/PDF export) and a structured **6-slide Board Deck**. |

---

## 🛠️ Prerequisites

Before running the installer on your workstation, ensure you have:

1. **CLI Tools Installed**:
   - `gcloud` (Google Cloud SDK, including `bq` and `gcloud beta`)
   - `python3` (3.11+)
   - `uv` ([Install uv](https://docs.astral.sh/uv/getting-started/installation/): `curl -LsSf https://astral.sh/uv/install.sh | sh`)
   - `jq` and `curl`

2. **Authenticated with Google Cloud & Google Drive Scope**:
   ```bash
   # 1. Authenticate gcloud with Google Drive access so the installer can upload
   #    the 2-page PDF, 85-row Excel, 2 RMA scans, and your Presenter Playbook
   #    directly into a folder in YOUR Google Drive:
   gcloud auth login --enable-gdrive-access

   # 2. Authenticate Application Default Credentials (ADC):
   gcloud auth application-default login
   ```

3. **A Gemini Enterprise App (Discovery Engine) in Your Project** *(Recommended)*:
   - If your GCP project already has a Gemini Enterprise app (in `global`, `eu`, or `us`), the installer will **auto-discover it** and register the agent automatically.

---

## 🚀 1-Command Setup & Deployment

Clone this repository and run `setup_and_deploy.sh`:

```bash
git clone https://github.com/papelamineG/ge-demo-google-store.git
cd ge-demo-google-store
bash setup_and_deploy.sh
```

### What `setup_and_deploy.sh` Does Automatically:
1. **Interactive `.env` Bootstrapper**: If no `.env` exists, it detects your active `gcloud` project and email (or lets you enter a custom `PROJECT_ID` and `REGION`) and writes `.env` for you.
2. **Pre-Flight Check (`--check` also available standalone)**: Verifies CLIs, active credentials, and quota alignment.
3. **API Enablement & Clean-Project IAM**: Enables required GCP APIs, initializes Google-managed service agents (Cloud Build, Cloud Run, Discovery Engine, Vertex AI), and grants required IAM roles.
4. **Parallel Data & Document Provisioning**:
   - Creates BigQuery dataset `demo_google_store_2654` and loads `customer_orders` (119 rows), `hub_inventory` (88 rows), `products_catalog` (22 rows), and `rma_defect_records` (35 rows) with full column descriptions and **Data Catalog / Knowledge Catalog** entries.
   - Seeds **Cloud Firestore** collection `demo-google-store-2654-tasks` with initial operational tasks (`TASK-101`, `TASK-102`, `TASK-103`).
   - Generates the **2-page QA Audit PDF** (`google-store_audit_report.pdf`), **85-row Carrier Discrepancy Excel** (`google-store_external_ledger.xlsx`), and **2 scanned RMA intake slips** (`google-store_simulated_order_task1.jpg`, `google-store_simulated_order_task2_discrepancy.jpg`), uploads them to **your Google Drive** and **your GCS bucket** (`<PROJECT_ID>-gstore-2654-docs`), and indexes them into a **Discovery Engine Unstructured Datastore**.
   - Provisions a dedicated **Vertex AI Agent Engine Code Execution Sandbox** for Prompt 7.
5. **Cloud Run Deployment & Gemini Enterprise Registration**:
   - Deploys the **Operations Console & Data Viewer** (`ge-viewer-google-store-2654`) and the **ADK Multi-Agent Backend** (`ge-agent-google-store-2654`) to Cloud Run.
   - Auto-discovers your Gemini Enterprise app and registers `Google Store Operations Assistant (2654)` (automatically cleaning up any older duplicate registrations).
6. **Autonomous Verification & Personalized Presenter Playbook**:
   - Runs end-to-end health checks across BigQuery, Firestore, Cloud Run, and Discovery Engine.
   - Generates **your personalized `GEMINI_ENTERPRISE_DEMO_SCRIPT.md` and `external_files/GEMINI_ENTERPRISE_DEMO_SCRIPT.pdf`** populated with **your** live Gemini Enterprise Chat URL, **your** BigQuery Studio URL, **your** Operations Console URL, and **your** Google Drive document links, and uploads both to your Google Drive folder!

---

## 🔍 Dry-Run Pre-Flight Check Only (`--check`)

To verify your local tools (`gcloud`, `bq`, `python3`, `uv`, `jq`) and GCP authentication without deploying any resources:

```bash
bash setup_and_deploy.sh --check
```

---

## 🔄 Resetting the Demo Between Live Runs (~10 Seconds)

Because **Prompt 5** mutates BigQuery (`hub_inventory`) and Firestore (`TASK-101`), and **Prompt 6** completes `TASK-102` in Firestore, you can reset all databases back to their pristine initial state in **~10 seconds** without redeploying Cloud Run:

```bash
bash scripts/reset_demo_state.sh
```

After running `reset_demo_state.sh`, click **"+ New Chat"** in Gemini Enterprise and refresh your Operations Console tab.

---

## 🧹 Teardown & Cleanup

To remove all demo resources created in your GCP project (Gemini Enterprise agent registration, Cloud Run services, Agent Engine Sandbox, Discovery Engine datastores, BigQuery dataset, Firestore collection, GCS bucket, and Google Drive folder):

```bash
bash scripts/cleanup.sh
```
