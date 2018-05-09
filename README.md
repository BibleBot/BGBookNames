BGBookNames
===========

A quick way of getting all the book names from all of Bible Gateway's versions. It's self-optimizing, removing duplicates and error resolution interactively (i.e. when it gets a book name that it doesn't know about). It takes about 72s to run, but I have plans to make this multithreaded.

## Installation

```bash
git clone https://github.com/BibleBot/BGBookNames
cd BGBookNames
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/start.py
```