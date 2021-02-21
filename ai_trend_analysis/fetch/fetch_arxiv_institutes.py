# Fetch arXiv / Grid data about institutional affiliation of researchers
import pandas as pd
import logging
import requests
import os
from zipfile import ZipFile
from io import BytesIO
from data_getters.arxiv_grid import get_arxiv_grid
from dotenv import load_dotenv, find_dotenv
import ai_trend_analysis

project_dir = ai_trend_analysis.project_dir

load_dotenv(find_dotenv())

config_path = os.getenv("config_path")

ARXIV_GRID_PATH = f"{project_dir}/data/arxiv/arxiv_grid.csv"
GRID_PATH = f"{project_dir}/data/secondary/grid"


def fetch_arxiv_grid():

    if os.path.exists(ARXIV_GRID_PATH) is False:
        logging.info("Collecting arXiv org data")
        arx_g = get_arxiv_grid(config_path, all_articles=True, include_mag_authors=True)
        arx_g.to_csv("ARXIV_GRID_PATH")

        # Collect the grid data (if necessary)
    else:
        logging.info("Already collected arXiv GRID data")

    if os.path.exists(GRID_PATH) is False:
        logging.info("Collecting Grid data")
        os.mkdir(GRID_PATH)
        g = requests.get(
            "https://digitalscience.figshare.com/ndownloader/files/23552738"
        )
        g_z = ZipFile(BytesIO(g.content))
        g_z.extractall(GRID_PATH)
    else:
        logging.info("Already collected GRID data")


def process_arxiv_grid():
    logging.info("Adding org types to arXiv grid data")
    arxiv_grid = pd.read_csv(ARXIV_GRID_PATH, dtype={"article_id": str})

    grid_types = (
        pd.read_csv(f"{GRID_PATH}/full_tables/types.csv")
        .set_index("grid_id")["type"]
        .to_dict()
    )
    arxiv_grid["org_type"] = arxiv_grid["institute_id"].map(grid_types)

    arxiv_grid.to_csv(ARXIV_GRID_PATH)


if __name__ == "__main__":
    fetch_arxiv_grid()
    process_arxiv_grid()
