AI trend analysis
==============================

Code to automate the generation of reports about the evolution of research trends in arXiv

# Installation

Run `make create_environment` to create a virtual environment and install all dependencies

# Data collection and processing

* Fetch data (includes scraping paper ids from DeepMind and OpenAI websites): `python ai_trend_analysis/fetch_data.py`
* Process data (includes finding AI papers): `python ai_trend_analysis/process_data.py`

--------

<p><small>Project based on the <a target="_blank" href="https://github.com/nestauk/cookiecutter-data-science-nesta">Nesta cookiecutter data science project template</a>.</small></p>
