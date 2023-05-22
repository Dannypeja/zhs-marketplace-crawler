import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import sqlite3
from sqlite3 import Connection, Error
from hashlib import md5
from urllib import parse as urlparse

# telegram bot support
import requests

def telegram_bot_sendtext(bot_message):

    bot_token = '5903579103:AAG5t5PmaMULZtXjG84vyIm-MGsC9epxq94'
    bot_chatID = '11527907'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

# create DB and connection
def create_connection(path: str) -> Connection:
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection
connection = create_connection("./marktplatz.db")
cursor = connection.cursor()

# driver setup
options = webdriver.ChromeOptions()
options.headless = True
# change if os is docker
SECRET_KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if SECRET_KEY:
    options.add_argument('--no-sandbox')
    options.binary_location = "/usr/bin/chromium-browser"


driver = webdriver.Chrome(options=options)

# checks if entry in table exists, based on hash
# returns False if entry already existed and no entry was added
def add_new_entry(checksum: hash, text: str) -> bool:
    count = connection.execute("SELECT COUNT() FROM Marktplatz WHERE checksum = ?;", (checksum,)).fetchall()[0][0]
    if count == 0:
        print("hash: " + checksum[:7] + " not in db: adding new one")
        connection.execute("INSERT INTO Marktplatz VALUES(?,?);", (checksum, text))
        connection.commit()
        return True
    else:
        print("hash: " + checksum[:7] + " already in DB")
        return False


# check first page
driver.get("https://www.buchung.zhs-muenchen.de/cgi/sportpartnerboerse.cgi?action=search&offset=0&sportart=Wassersport&koennen=")
driver.implicitly_wait(0.5)

# find all texts on one page
descriptions = driver.find_elements_by_class_name("sp3")
# add to database
for description in descriptions:
  text = description.text
  checksum = md5(text.encode()).hexdigest()

  if add_new_entry(checksum, text): # adds new entry and returns True
      # sends email with text and link to click
      print("Triggered Telegram message.")
      ascii_safe_text = urlparse.quote_plus(text)
      ascii_safe_url = url = urlparse.quote_plus("https://www.buchung.zhs-muenchen.de/cgi/sportpartnerboerse.cgi?action=search&offset=0&sportart=Wassersport&koennen=")
      telegram_bot_sendtext("New entries on page: \n" + ascii_safe_text + "\n" + ascii_safe_url)

driver.close()

