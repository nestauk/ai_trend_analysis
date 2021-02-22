import os
import json
import yaml
import logging
import pickle
from gensim.models import FastText

import ai_trend_analysis

project_dir = ai_trend_analysis.project_dir

with open(f"{project_dir}/model_config.yaml", "r") as infile:
    min_count = yaml.safe_load(infile)["min_count"]


def train_word2vec():

    if os.path.exists(f"{project_dir}/models/word2vec.p") is True:
        logging.info("Already trained model")
    else:
        logging.info("loading and processing data")
        with open(f"{project_dir}/data/arxiv/arxiv_tokenised.json", "r") as infile:
            arxiv_tokenised = json.load(infile)

        tok = list(arxiv_tokenised.values())

        logging.info("Training model")
        ft = FastText(tok, min_count=min_count, word_ngrams=0)

        # Save model
        with open(f"{project_dir}/models/word2vec.p", "wb") as outfile:
            pickle.dump(ft, outfile)


if __name__ == "__main__":
    train_word2vec()
