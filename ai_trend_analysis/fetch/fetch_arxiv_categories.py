# Fetch arXiv category code - name lookup
import os
import json
import logging
from data_getters.core import get_engine
from dotenv import load_dotenv, find_dotenv
import pandas as pd
import ai_trend_analysis

project_dir = ai_trend_analysis.project_dir

load_dotenv(find_dotenv())

CAT_LOOKUP_PATH = f"{project_dir}/data/metadata/arxiv_category_lookup.json"


def fetch_arxiv_category_lookup():
    if os.path.exists(CAT_LOOKUP_PATH) is False:
        config_path = os.getenv("config_path")
        con = get_engine(config_path)
        c = pd.read_sql("arxiv_categories", con)

        # We create a lookup between arXiv categories and descriptions
        arxiv_lookup = c.set_index("id")["description"].to_dict()

        # If the description if missing we keep the cat code as description
        arxiv_lookup = {
            (k): (": ".join([k, v]) if v != None else k)
            for k, v in arxiv_lookup.items()
        }

        with open(CAT_LOOKUP_PATH, "w") as outfile:
            json.dump(arxiv_lookup, outfile)
    else:
        logging.info("Already collected arXiv categories")


if __name__ == "__main__":
    fetch_arxiv_category_lookup()
