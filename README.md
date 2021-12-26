# NotionWiki
[![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/tterb%2FHyde)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![](https://img.shields.io/github/workflow/status/nccassady/NotionWiki/Python%20application)
[![Documentation Status](https://readthedocs.org/projects/notionwiki/badge/?version=latest)](https://notionwiki.readthedocs.io/en/latest/?badge=latest)

This project uses the Notion and Wikipedia APIs to populate data in Notion based on Wikidata properties.

## Installation
1. Install requirements:
    >`pip install -r requirements.txt`

2. Set your API key and Database ID in the following environment variables, respectively:
   - `api_secret`
   - `database_id`

## Use
`python app.py`