import schedule
import time
from bot import Bot
from sheet.sheet import get_deadlines


def job():
    deadlines = get_deadlines()

    bot = Bot()
    bot.post_message(deadlines)

schedule.every().day.at('01:00').do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
