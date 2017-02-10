from bot import Bot
from sheet.sheet import get_deadlines


def test_bot():
    deadlines = get_deadlines()

    bot = Bot(debug=False)
    bot.post_message(deadlines)
