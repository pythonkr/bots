from bot import Bot
import schedule
from sheet.sheet import get_deadlines


def job():
    deadlines = get_deadlines()

    bot = Bot()
    bot.post_message(deadlines)

schedule.every().day.at('01:00').do(job)
