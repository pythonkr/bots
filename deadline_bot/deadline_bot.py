from config import SLACK_BOT_TOKEN
from slacker import Slacker
from sheet.sheet import get_deadlines
from logger import logger

slacker = Slacker(SLACK_BOT_TOKEN)

for deadline in get_deadlines():
    try:
        message = ''
        if deadline.remain_day > 0:
            message = '```{}``` {} 님 작업 마감이 {}일 남았습니다'.format(deadline.work,
                    deadline.worker,
                    deadline.remain_day)
        elif deadline.remain_day == 0:
            message = '```{}``` {} 님 작업 마감일입니다'.format(deadline.work, deadline.worker)
        else:
            message = '```{}``` {} 님 작업 마감이 {}일 지났습니다'.format(deadline.work,
                    deadline.worker
                    -deadline.remain_day)
        slacker.chat.post_message('#' + deadline.channel, message, as_user=True)
    except Exception as e:
        logger.warn('Error: {}'.format(e))
        logger.warn('Deadline: {}'.format(deadline))
