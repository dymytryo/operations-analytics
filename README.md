# Operations Analytics Portfolio

Focused operations and supply-chain analytics projects that demonstrate cost modeling, vendor comparison, inventory decisions, practical process improvement, and the data engineering that keeps operations teams out of manual work.

This repository is intentionally organized as a portfolio collection, not as an installable package. Each project should stand alone with a concise README, cleaned shareable artifacts, and enough context to explain the operational decision logic.

## Projects

| Project | Techniques | Portfolio Signal |
| --- | --- | --- |
| [Inventory Management Case Study](projects/inventory-management-case-study) | Quantity discount model, EOQ reasoning, vendor comparison, cost optimization | Inventory planning, procurement analytics, operational cost reduction |
| [Project Management Order-Picking System](projects/project-management-order-picking-system) | PERT, CPM, critical path, schedule risk | Project planning, timeline optimization, risk-based delivery recommendations |
| [Google Sheets ⇄ Data Lake: Operational Reverse ETL](projects/sheets-to-lake-reverse-etl) | Sheets API OAuth, batched Athena enrichment, Parquet CTAS, idempotent appends, scheduled SageMaker execution | Operational data engineering: reverse ETL, pipeline hardening, self-serve reporting for ops teams |

## Repository Pattern

Each project should keep a simple structure:

```text
projects/<project-name>/
├── README.md
├── data/
├── diagrams/
└── docs/
```

Use `data/` only for cleaned, shareable summary artifacts. Keep raw Office exports, classroom reports, workbook metadata, and files with personal metadata out of the public repo.

## Future Project Ideas

- Inventory reorder-point examples
- Vendor scorecard and procurement analysis
- Warehouse or fulfillment cost analysis
- Demand planning and capacity scenarios
- Service-level tradeoff analysis
