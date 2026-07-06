"""Load processed datasets into PostgreSQL."""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from src.utils.config import get_settings
from src.utils.logger import get_logger


logger = get_logger(__name__)


def load_csv_to_postgres(csv_path: Path, table_name: str) -> None:
    """Load a CSV file into a PostgreSQL table."""
    settings = get_settings()
    engine = create_engine(settings.postgres_url)

    logger.info("Loading %s into table %s", csv_path, table_name)
    dataframe = pd.read_csv(csv_path)
    dataframe.to_sql(table_name, engine, if_exists="replace", index=False)
    logger.info("Loaded %s rows into %s", len(dataframe), table_name)


if __name__ == "__main__":
    load_csv_to_postgres(Path("data/raw/bcb/selic.csv"), "bcb_selic")
