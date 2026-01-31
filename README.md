# SCD2 Pipeline - Databricks Asset Bundle

Deploy your SCD2 (Slowly Changing Dimension Type 2) pipeline from **hilton_hotmail** (dev) to **prod_2** (prod) via GitHub and Databricks Asset Bundles.

## Structure

```
├── databricks.yml          # Bundle config, dev/prod targets
├── scd2/                   # SCD2 pipeline assets
│   ├── scd2.yaml           # Pipeline config (notebook path reference)
│   ├── scd2-pipeline.yml   # DLT pipeline definition
│   ├── scd2-job.yml        # Job to refresh pipeline
│   └── transformations/   # SCD2 pipeline logic
│       ├── __init__.py
│       └── scd2_pipeline.py
├── .github/
│   └── workflows/
│       ├── deploy-dev.yml
│       └── deploy-prod.yml
└── README.md
```

## Local Setup

1. **Install Databricks CLI** (v0.283+): https://docs.databricks.com/dev-tools/cli/install
2. **Authenticate**: `databricks auth login` (for each workspace)
3. **Validate**: `databricks bundle validate`
4. **Deploy to dev**: `databricks bundle deploy -t dev`
5. **Deploy to prod**: `databricks bundle deploy -t prod`

## GitHub CI/CD

Configure these in your GitHub repo:

**Secrets:**
- `DATABRICKS_TOKEN` - Service principal or user access token

**Variables:**
- `DATABRICKS_HOST` - Prod workspace URL (e.g. `https://dbc-c382fa4e-0ede.cloud.databricks.com`)
- `DATABRICKS_HOST_DEV` - Dev workspace URL (e.g. `https://dbc-3a9c6033-1f4e.cloud.databricks.com`)

- **Push to `main`** → Deploys to prod_2
- **Push to `develop`** or **PR to main** → Deploys to hilton_hotmail (dev)

## Raw Data

The pipeline reads from `raw_source`. Update `scd2/transformations/scd2_pipeline.py` to point to your data:

- **Delta table**: `spark.read.format("delta").table("catalog.schema.table")`
- **Volume**: `spark.read.format("delta").load("/Volumes/catalog/schema/volume/path")`

Raw datasets are not included in the bundle; ensure data exists in the target workspace/catalog before running.
