import ai_trend_analysis
import pandas as pd
import logging
import os

project_dir = ai_trend_analysis.project_dir

INST_PATH = f"{project_dir}/arxiv/processed/arxiv_institutes.csv"

def process_arxiv_grid():
    """Tidy up the institute data to remove corp duplicates"""
    if os.path.exists(INST_PATH):
        logging.info("Making institute dataset")
        arx_g = pd.read_csv(
            f"{project_dir}/data/arxiv/processed/arxiv_grid.csv",
            dtype={"article_id": str},
        )

        arx_g = arx_g.dropna(axis=0, subset=["institute_name"])

        arx_g["institute_name"] = [
            x.split("(")[0].strip() if " (" in x else x for x in arx_g["institute_name"]
        ]

        arx_no_dupes = arx_g.drop_duplicates(
            ["article_id", "institute_name"]
        ).reset_index(drop=False)

        arx_no_dupes_sel = arx_no_dupes[
            [
                "article_id",
                "article_title",
                "institute_name",
                "institute_country",
                "is_ai",
                "org_type",
            ]
        ]

        arx_no_dupes_sel.to_csv(INST_PATH, index=False)
    else:
        logging.info("already processed institute data")


if __name__ == "__main__":
    process_arxiv_grid()
