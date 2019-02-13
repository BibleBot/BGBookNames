name_scraper
===========

A quick way of getting all the book names from all the versions of Bible Gateway and API.Bible. It's self-optimizing, removing duplicates and error resolution interactively (i.e. when it gets a book name that it doesn't know about). It takes about 72s to run, but I have plans to make this multithreaded.

## Installation

```bash
git clone https://github.com/BibleBot/name_scraper
cd name_scraper
python3 -m venv venv
source venv/bin/activate
pip install -U bs4 colorama lxml requests
python src/start.py
```