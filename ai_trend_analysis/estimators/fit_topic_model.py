from ai_trend_analysis.hSBM_Topicmodel.sbmtm import sbmtm
from ai_trend_analysis.transformers.create_topic_df import (
    post_process_model,
    filter_topics,
)
from ai_trend_analysis.getters import (
    get_articles,
    get_article_categories,
    make_category_sets,
    get_tokenised,
)
import yaml
import os
import pickle
import logging
import ai_trend_analysis

project_dir = ai_trend_analysis.project_dir


def filter_tokenised(tok, id_set):
    """Filter tokenised abstracts based on ids"""
    return {k: v for k, v in tok.items() if k in id_set}


def train_model(_dict):
    """Fits a hierarchical topic model to the data"""

    docs = list(_dict.values())
    _ids = list(_dict.keys())

    logging.info("Training model")
    topic_model = sbmtm()
    topic_model.make_graph(docs, documents=_ids)
    topic_model.fit()

    logging.info("Processing outputs")

    topic_post = post_process_model(topic_model, top_level=0)

    topic_mix_sel = filter_topics(topic_post[0], presence_thr=0.05, prevalence_thr=0.3)

    print(topic_mix_sel[1])
    return topic_post[1], topic_mix_sel[0]


if __name__ == "__main__":

    # Categories we want to topic model
    with open(f"{project_dir}/model_config.yaml", "r") as infile:
        my_cats = yaml.safe_load(infile)["case_categories"]

    logging.info(my_cats)

    # Read data
    art = get_articles()
    cats = get_article_categories()
    tok = get_tokenised()
    cat_sets = make_category_sets(cats)

    for c in my_cats:
        logging.info(f"Processing {c[0]}")
        # c[1] has whether we want to focus on papers in AI nor not
        if c[1] is False:
            ids = cat_sets[c[0]]
            tok_sel = filter_tokenised(tok, ids)
        else:
            ids = set(cat_sets[c[0]]) & set(art.query("is_ai==True")["article_id"])
            tok_sel = filter_tokenised(tok, ids)

        logging.info(len(ids))
        model_output = train_model(tok_sel)
        with open(f"{project_dir}/data/models/{c[0]}.p", "wb") as outfile:
            pickle.dump(model_output, outfile)
