from bot import Bot
from sheet.sheet import get_deadlines

deadlines = get_deadlines()

bot = Bot()
bot.post_message(deadlines)
