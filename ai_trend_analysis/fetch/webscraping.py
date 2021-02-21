import os
import yaml
import requests
import json
import logging
from time import sleep
import ai_trend_analysis
import re
from bs4 import BeautifulSoup

project_dir = ai_trend_analysis.project_dir

with open(project_dir / "model_config.yaml", "rt") as f:
    config = yaml.safe_load(f.read())["webscrapes"]


SCRAPED_PATH = f"{project_dir}/data/scraped/scraped_arxiv.json"


def webscraping():
    if os.path.exists(SCRAPED_PATH) is True:
        logging.info("Already scraped DM / OpenAI data")

    else:
        logging.info("Scraping deepmind publications")

        # Collect the DeepMind arXiv papers

        DM_URL = config["dm_url"]
        DM_PAGES = config["n_pages"]

        dm_arx = []

        for p in range(1, DM_PAGES):

            sleep(2)

            dm_page = requests.get(DM_URL.format(t=p))
            content = (dm_page.content).decode()
            parsed = json.loads(content[6:])

            for r in parsed["results"]:
                if "download" in r.keys():
                    url = r["download"]
                    if "arxiv" in str(url):
                        # Change links to pdfs to links to abstracts
                        if url[-4:] == ".pdf":  # Removes pdf format
                            url = url[:-4]
                        url = re.sub("pdf", "abs", url)
                        dm_arx.append(url)

        # Collect OpenAI papers
        logging.info("Scraping openai publications")

        oai_url = config["oai_url"]

        # Download and parse the data
        oai = BeautifulSoup(requests.get(oai_url).content, features="lxml")

        # Unique links in the page that contain arXiv
        oai_arx = set(
            [x for x in [x.get("href") for x in oai.find_all("a")] if "arxiv" in x]
        )

        # Conclude
        dm_lu = {x: "DeepMind" for x in dm_arx}
        oai_lu = {x: "OpenAI" for x in oai_arx}

        combined = {**dm_lu, **oai_lu}

        with open(SCRAPED_PATH, "w") as outfile:
            json.dump(combined, outfile)


if __name__ == "__main__":

    webscraping()
