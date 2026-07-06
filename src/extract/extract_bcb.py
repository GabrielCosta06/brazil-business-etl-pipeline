import json
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


BCB_SERIES = {
    "selic_daily": {
        "code": 11,
        "description": "Selic daily interest rate",
        "frequency": "daily"
    },
    "usd_brl_daily": {
        "code": 1,
        "description": "USD/BRL exchange rate, selling price",
        "frequency": "daily"
    },
    "ipca_monthly": {
        "code": 433,
        "description": "IPCA monthly inflation rate",
        "frequency": "monthly"
    }
}


def extract_bcb_series(
    series_code: int,
    series_name: str,
    start_date: str,
    end_date: str
) -> pd.DataFrame:
    """
    Extracts a time series from Banco Central do Brasil SGS API.

    Parameters:
        series_code: BCB SGS series code.
        series_name: Friendly name for the indicator.
        start_date: Start date in dd/mm/yyyy format.
        end_date: End date in dd/mm/yyyy format.

    Returns:
        DataFrame containing the extracted time series.
    """

    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_code}/dados"
        f"?formato=json&dataInicial={start_date}&dataFinal={end_date}"
    )

    logging.info(f"Extracting {series_name} | code {series_code}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"Request failed for {series_name}: {error}")
        raise

    except json.JSONDecodeError as error:
        logging.error(f"Invalid JSON returned for {series_name}: {error}")
        raise

    df = pd.DataFrame(data)

    if df.empty:
        logging.warning(f"No data returned for {series_name}")
        return df

    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

    df["series_code"] = series_code
    df["series_name"] = series_name
    df["extracted_at"] = datetime.now()

    df = df[
        [
            "series_code",
            "series_name",
            "data",
            "valor",
            "extracted_at"
        ]
    ]

    logging.info(f"Extracted {len(df)} rows for {series_name}")

    return df


def save_dataframe(df: pd.DataFrame, output_path: Path, file_name: str) -> None:
    """
    Saves a DataFrame as CSV.
    """

    output_path.mkdir(parents=True, exist_ok=True)

    full_path = output_path / file_name
    df.to_csv(full_path, index=False)

    logging.info(f"Saved file: {full_path}")


def save_metadata(output_path: Path) -> None:
    """
    Saves metadata about the extracted BCB series.
    """

    metadata = []

    for series_name, details in BCB_SERIES.items():
        metadata.append(
            {
                "series_name": series_name,
                "series_code": details["code"],
                "description": details["description"],
                "frequency": details["frequency"]
            }
        )

    metadata_df = pd.DataFrame(metadata)
    save_dataframe(metadata_df, output_path, "bcb_series_metadata.csv")


def run_bcb_extraction(start_date: str, end_date: str) -> None:
    """
    Runs the full BCB extraction process.
    """

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path("data/raw/bcb") / run_id

    all_dataframes = []

    logging.info("Starting BCB extraction pipeline")
    logging.info(f"Date range: {start_date} to {end_date}")
    logging.info(f"Run ID: {run_id}")

    for series_name, details in BCB_SERIES.items():
        df = extract_bcb_series(
            series_code=details["code"],
            series_name=series_name,
            start_date=start_date,
            end_date=end_date
        )

        if not df.empty:
            file_name = f"{series_name}.csv"
            save_dataframe(df, output_path, file_name)
            all_dataframes.append(df)

    if all_dataframes:
        consolidated_df = pd.concat(all_dataframes, ignore_index=True)
        save_dataframe(consolidated_df, output_path, "bcb_consolidated.csv")

    save_metadata(output_path)

    logging.info("BCB extraction pipeline finished successfully")


if __name__ == "__main__":
    run_bcb_extraction(
        start_date="01/01/2024",
        end_date=datetime.now().strftime("%d/%m/%Y")
    )