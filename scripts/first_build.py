from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import sqlite3
from sqlite3 import Connection, Error
from hashlib import md5
import os


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

# create Table
cursor.execute("CREATE TABLE if not exists Marktplatz(checksum, text)")

# driver setup
options = webdriver.ChromeOptions()
options.headless = True

# change if os is docker
SECRET_KEY = os.environ.get("AM_I_IN_A_DOCKER_CONTAINER", False)

if SECRET_KEY:
    print("I am running in a Docker container")
    options.add_argument("--no-sandbox")
    options.binary_location = "/usr/bin/chromium-browser"

driver = webdriver.Chrome(options=options)


# checks if entry in table exists, based on hash
# returns False if entry already existed and no entry was added
def add_new_entry(checksum: hash, text: str) -> bool:
    count = connection.execute(
        "SELECT COUNT() FROM Marktplatz WHERE checksum = ?;", (checksum,)
    ).fetchall()[0][0]
    if count == 0:
        print("hash: " + checksum[:7] + " not in db: adding new one")
        connection.execute("INSERT INTO Marktplatz VALUES(?,?);", (checksum, text))
        connection.commit()
        return True
    else:
        print("hash: " + checksum[:7] + " already in DB")
        return False


# begin crawl of all pages
driver.get(
    "https://www.buchung.zhs-muenchen.de/cgi/sportpartnerboerse.cgi?action=search&offset=0&sportart=Wassersport&koennen="
)
driver.implicitly_wait(0.5)

# find count of pages
pagesCount = len(driver.find_elements(By.XPATH, "//b"))


# go over all pages
for i in range(0, pagesCount + 1):
    driver.get(
        "https://www.buchung.zhs-muenchen.de/cgi/sportpartnerboerse.cgi?action=search&offset="
        + str(i)
        + "&sportart=Wassersport&koennen="
    )

    # find all texts on one page
    descriptions = driver.find_elements_by_class_name("sp3")
    # add to database
    for description in descriptions:
        text = description.text
        checksum = md5(text.encode()).hexdigest()
        add_new_entry(checksum, text)

driver.close()
