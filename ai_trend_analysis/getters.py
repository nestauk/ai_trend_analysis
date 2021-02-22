# Data getters
import ai_trend_analysis
import pandas as pd
import json

project_dir = ai_trend_analysis.project_dir


def get_articles():
    """Gets arXiv articles"""
    return pd.read_csv(
        f"{project_dir}/data/arxiv/processed/arxiv_articles.csv",
        dtype={"article_id": str},
    )


def get_institutes():
    """Gets arxiv institutes"""
    return pd.read_csv(
        f"{project_dir}/data/arxiv/processed/arxiv_institutes.csv",
        dtype={"article_id": str},
    )


def get_article_categories():
    """Gets article categories"""
    return pd.read_csv(
        f"{project_dir}/data/arxiv/arxiv_article_categories.csv",
        dtype={"article_id": str},
    )


def make_category_sets(cats):
    """Create category sets"""

    return cats.groupby("category_id")["article_id"].apply(lambda x: set(x)).to_dict()


def get_category_names():
    """Get arXiv category - name lookup"""
    with open(f"{project_dir}/data/metadata/arxiv_category_lookup.json", "r") as infile:
        return json.load(infile)


def get_tokenised():
    """Get tokenised abstracts"""
    with open(f"{project_dir}/data/arxiv/arxiv_tokenised.json", "r") as infile:
        return json.load(infile)


def filter_tokenised(tok, id_set):
    """Filter tokenised abstracts based on ids"""
    return {k: v for k, v in tok.items() if k in id_set}
