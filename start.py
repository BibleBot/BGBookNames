'''
    Copyright (c) 2018 Elliott Pardee <me [at] vypr [dot] xyz>
    This file is part of BGBookNames.

    BGBookNames is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    BGBookNames is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with BGBookNames.  If not, see <http://www.gnu.org/licenses/>.
'''

import asyncio
import requests
import json
import os
import sys
from bs4 import BeautifulSoup
import logging
from http.client import HTTPConnection
HTTPConnection.debuglevel = 0

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/")

from vylogger import VyLogger

logger = VyLogger("default")

versionsURL = "https://www.biblegateway.com/versions/"
extensionsURL = "https://abbv.biblebot.xyz/extensions.json"

bookNames = {
    "gen": [],
    "exod": [],
    "lev": [],
    "num": [],
    "deut": [],
    "josh": [],
    "judg": [],
    "ruth": [],
    "1sam": [],
    "2sam": [],
    "1kgs": [],
    "2kgs": [],
    "1chr": [],
    "2chr": [],
    "ezra": [],
    "neh": [],
    "esth": [],
    "job": [],
    "ps": ["Psalms"],
    "prov": [],
    "eccl": [],
    "song": [],
    "isa": [],
    "jer": [],
    "lam": [],
    "ezek": [],
    "dan": [],
    "hos": [],
    "joel": [],
    "amos": [],
    "obad": [],
    "jonah": [],
    "mic": [],
    "nah": [],
    "hab": [],
    "zeph": [],
    "hag": [],
    "zech": [],
    "mal": [],
    "matt": [],
    "mark": [],
    "luke": [],
    "john": [],
    "acts": [],
    "rom": [],
    "1cor": [],
    "2cor": [],
    "gal": [],
    "eph": [],
    "phil": [],
    "col": [],
    "1thess": [],
    "2thess": [],
    "1tim": [],
    "2tim": [],
    "titus": [],
    "phlm": [],
    "heb": [],
    "jas": [],
    "1pet": [],
    "2pet": [],
    "1john": [],
    "2john": [],
    "3john": [],
    "jude": [],
    "rev": [],
    "tob": [],
    "jdt": [],
    "gkest": [],
    "wis": [],
    "sir": [],
    "bar": [],
    "epjer": [],
    "praz": [],
    "sus": [],
    "bel": [],
    "1macc": [],
    "2macc": [],
    "1esd": [],
    "prman": [],
    "ps151": [],
    "3ma": [],
    "2esd": [],
    "4ma": [],
}

res = requests.get(versionsURL)

obj = {}

ignoredTranslations = ["Arabic Bible: Easy-to-Read Version (ERV-AR)", "Ketab El Hayat (NAV)",
                       "Farsi New Testament", "Farsi Ebook Bible", "Habrit Hakhadasha/Haderekh (HHH)",
                       "The Westminster Leningrad Codex (WLC)", "Urdu Bible: Easy-to-Read Version (ERV-UR)",
                       "Hawai‘i Pidgin (HWP)"]


def logMessage(level, msg):
    message = "[shard 0] <" + \
        "BGBookNames@global> " + msg

    if level == "warn":
        logger.warning(message)
    elif level == "err":
        logger.error(message)
    elif level == "info":
        logger.info(message)
    elif level == "debug":
        logger.debug(message)


def getBooks():
    if res is not None:
        soup = BeautifulSoup(res.text, "html.parser")

        logMessage("info", "Getting translations...")

        for translation in soup.findAll("td", {"class": ["collapse", "translation-name"]}):
            for a in translation.findAll("a", href=True):
                version = a.text
                link = a["href"]

                if "#booklist" in link and version not in ignoredTranslations:
                    obj[version] = {}
                    obj[version]["booklist"] = "https://www.biblegateway.com" + link

        if obj is not {}:
            logMessage("info", "Getting book names... (this will take a while)")
            for item in obj:
                booklistURL = obj[item]["booklist"]
                bookRes = requests.get(booklistURL)

                if bookRes is not None:
                    soup = BeautifulSoup(bookRes.text, "html.parser")

                    table = soup.find("table", {"class": "chapterlinks"})

                    for tableField in table.findAll("td"):
                        book = dict(tableField.attrs).get("data-target")

                        for chapterNumbers in tableField.findAll("span", {"class": "num-chapters"}):
                            chapterNumbers.decompose()

                        if not str(book) == "None":
                            book = book[1:-5]
                            classes = dict(tableField.attrs).get("class")

                            try:
                                if book == "3macc":
                                    book = "3ma"
                                elif book == "gkesth" or book == "adest":
                                    book = "gkest"
                                elif book == "sgthree" or book == "sgthr":
                                    book = "praz"

                                if "book-name" in classes:
                                    if tableField.text not in bookNames[book]:
                                        bookNames[book].append(tableField.text)
                            except KeyError:
                                logMessage("err", "found " +
                                           book + " in " + item)
                                book = input(
                                    "[bfix] what should I rename this book to?")

                                if not book == "":
                                    if tableField.text not in bookNames[book]:
                                        bookNames[book].append(tableField.text)

        if os.path.isfile(dir_path + "/books.json"):
            logMessage("info", "Found books.json, removing...")
            os.remove(dir_path + "/books.json")

        with open(dir_path + "/books.json", "w") as file:
            logMessage("info", "Writing file...")
            file.write(json.dumps(bookNames))


if __name__ == "__main__":
    getBooks()
