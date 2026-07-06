# Architecture

This project is organized as a simple ETL pipeline for Brazilian business data.

- `src/extract`: data extraction scripts.
- `src/load`: database loading scripts.
- `src/utils`: shared configuration and logging helpers.
- `data/raw`: raw downloaded data.
- `data/processed`: transformed datasets.
- `sql`: database schema and setup scripts.
- `dbt`: dbt project files.
- `dags`: orchestration DAGs.
- `powerbi`: dashboard assets and screenshots.
