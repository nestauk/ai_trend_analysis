from ai_trend_analysis.transformers.arxiv_tokenise import arxiv_tokenise
from ai_trend_analysis.transformers.train_word2vec import train_word2vec
from ai_trend_analysis.transformers.find_ai_papers import find_ai_papers
from ai_trend_analysis.transformers.process_paper_data import (
    process_paper_data,
    process_arxiv_grid,
)


def process_data():
    arxiv_tokenise()
    train_word2vec()
    find_ai_papers()
    process_paper_data()
    process_arxiv_grid()


if __name__ == "__main__":
    process_data()
