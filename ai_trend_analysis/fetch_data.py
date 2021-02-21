from ai_trend_analysis.fetch.fetch_arxiv import fetch_arxiv_tables
from ai_trend_analysis.fetch.fetch_arxiv_categories import fetch_arxiv_category_lookup
from ai_trend_analysis.fetch.fetch_arxiv_institutes import (
    fetch_arxiv_grid,
    process_arxiv_grid,
)
from ai_trend_analysis.fetch.webscraping import webscraping

if __name__ == "__main__":
    fetch_arxiv_tables()
    fetch_arxiv_category_lookup()
    fetch_arxiv_grid()
    process_arxiv_grid()
    webscraping()
