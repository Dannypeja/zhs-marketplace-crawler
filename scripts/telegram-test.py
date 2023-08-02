import requests
from urllib import parse as urlparse


def telegram_bot_sendtext(bot_message):
    bot_token = "5903579103:AAG5t5PmaMULZtXjG84vyIm-MGsC9epxq94"
    bot_chatID = "-1001963609086"
    #bot_chatID = "11527907"
    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + bot_chatID
        + "&parse_mode=Markdown&text="
        + bot_message
    )

    response = requests.get(send_text)

    return response.json()


text = "123"
url = "https://www.buchung.zhs-muenchen.de/cgi/sportpartnerboerse.cgi?action=search&offset=0&sportart=Wassersport&koennen="

url = urlparse.quote_plus(url)

telegram_bot_sendtext("*should be bold?* [Weiterleitung zur Kursplatzbörse](https://danilop.de/zhs-landing-page/)")
