# Brazil Business ETL Pipeline

## About the project

This is a portfolio project I’m building to practice and showcase data engineering and analytics skills.

The idea is to create an end-to-end pipeline that extracts Brazilian economic data, stores the raw files, loads the data into a database, transforms it, and later connects it to Power BI for analysis.

I currently work more with Power BI, DAX and SQL, so this project is also a way for me to improve my Python, ETL, PostgreSQL, dbt and orchestration skills.

## What the project does so far

Right now, the pipeline extracts public economic indicators from the Banco Central do Brasil SGS API.

The script extracts:

| Indicator     | Code | Description               |
| ------------- | ---: | ------------------------- |
| selic_daily   |   11 | Selic daily interest rate |
| usd_brl_daily |    1 | USD/BRL exchange rate     |
| ipca_monthly  |  433 | IPCA monthly inflation    |

After extracting the data, the pipeline saves the results as CSV files in a raw data folder.

Each pipeline run creates a new timestamped folder, so the raw data history is preserved.

## Current architecture

```text
Banco Central do Brasil API
        ↓
Python extraction script
        ↓
Raw CSV files
        ↓
Timestamped folder
        ↓
Consolidated CSV file
```

## Project structure

```text
brazil-business-etl-pipeline/
│
├── README.md
├── requirements.txt
├── .env.example
├── docker-compose.yml
├── .gitignore
│
├── src/
│   ├── extract/
│   │   └── extract_bcb.py
│   │
│   ├── load/
│   │   └── load_to_postgres.py
│   │
│   └── utils/
│       ├── config.py
│       └── logger.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── sql/
├── dbt/
├── dags/
├── powerbi/
└── docs/
```

## How to run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/brazil-business-etl-pipeline.git
cd brazil-business-etl-pipeline
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On Linux or macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the extraction script

```bash
python src/extract/extract_bcb.py
```

## Output

After running the script, a new folder is created inside:

```text
data/raw/bcb/
```

Example files generated:

```text
selic_daily.csv
usd_brl_daily.csv
ipca_monthly.csv
bcb_consolidated.csv
bcb_series_metadata.csv
```

The consolidated file contains all extracted indicators in one dataset.

## Current features

* Extracts data from the Banco Central do Brasil SGS API
* Saves raw data as CSV files
* Creates one folder per extraction run
* Creates a consolidated CSV file
* Creates a metadata file with the extracted indicators
* Includes basic logging and error handling

## Next steps

The next things I plan to build are:

* Load the raw files into PostgreSQL
* Create raw and staging tables
* Add simulated business sales data
* Transform the data using SQL and dbt
* Add basic data quality tests
* Orchestrate the pipeline with Airflow
* Build a Power BI dashboard using the final tables

## Skills I want to demonstrate

With this project, I want to show experience with:

* Python
* Pandas
* API extraction
* ETL pipeline structure
* SQL
* PostgreSQL
* Data modeling
* dbt
* Airflow
* Power BI
* Git and GitHub

## Why I’m building this

I’m building this project to go beyond only creating dashboards.

My goal is to better understand the full data workflow, from extracting and storing data to transforming it and creating insights for business analysis.

## Author

Gabriel

Junior Data Analyst developing skills in Data Engineering, Analytics Engineering and Business Intelligence.