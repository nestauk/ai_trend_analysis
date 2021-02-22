import os
import logging
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from data_getters.core import get_engine
import ai_trend_analysis

project_dir = ai_trend_analysis.project_dir

DATA_PATH = f"{project_dir}/data/arxiv"

load_dotenv(find_dotenv())

config_path = os.getenv("config_path")

#####
# Preamble
#####


def fetch_daps_table(table, con, chunks=1000):

    ch = pd.read_sql_table(table, con, chunksize=chunks)

    return pd.concat(ch).reset_index(drop=True)


#####
# Read arXiv data
#####


def fetch_arxiv_tables():
    # Connect to db
    con = get_engine(f"{config_path}")

    logging.info("Downloading data")

    for t in ["arxiv_article_categories", "arxiv_articles"]:

        # Read and save tables
        if os.path.exists(f"{DATA_PATH}/{t}.csv") is False:
            logging.info(f"Donwloading table: {t}")
            daps_t = fetch_daps_table(t, con, 1000)
            # Change column names
            if "id" in daps_t.columns:
                daps_t = daps_t.rename(columns={"id": "article_id"})
            daps_t.to_csv(f"{DATA_PATH}/{t}.csv", index=False)


if __name__ == "__main__":
    fetch_arxiv_tables()
