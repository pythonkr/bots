from slacker import Slacker
from sheet.sheet import get_deadlines
from config import SLACK_BOT_TOKEN

slacker = Slacker(SLACK_BOT_TOKEN)

for deadline in get_deadlines():
    message = ''
    if deadline.remain_day > 0:
        message = '```{}``` 작업 마감이 {}일 남았습니다'.format(deadline.work, deadline.remain_day)
    elif deadline.remain_day == 0:
        message = '```{}``` 작업 마감일입니다'.format(deadline.work)
    else:
        message = '```{}``` 작업 마감이 {}일 지났습니다'.format(deadline.work, -deadline.remain_day)
    slacker.chat.post_message('#random', message, as_user=True)
