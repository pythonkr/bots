from config import SLACK_BOT_TOKEN
from logger import logger
from sheet.deadline import Deadline
from slacker import Slacker
from typing import List


class Bot:
    def __init__(self):
        self.__slacker = Slacker(SLACK_BOT_TOKEN)

    def post_message(self, deadlines: List[Deadline]):
        for deadline in deadlines:
            if deadline.remain_day > 0:
                message = '```{}``` {} 님 작업 마감이 {}일 남았습니다'.format(
                    deadline.work,
                    deadline.worker,
                    deadline.remain_day)
                self.__post_message(deadline.channel, message)
            elif deadline.remain_day == 0:
                message = '```{}``` {} 님 작업 마감일입니다'.format(
                    deadline.work,
                    deadline.worker)
                self.__post_message(deadline.channel, message)
            else:
                message = '```{}``` {} 님 작업 마감이 {}일 지났습니다'.format(
                    deadline.work,
                    deadline.worker,
                    -deadline.remain_day)
                self.__post_message(deadline.channel, message)

    def __post_message(self, channel, message):
        try:
            self.__slacker.chat.post_message('#' + channel, message, as_user=True, link_names=1)
        except Exception as e:
            logger.warn('error: {}, channel: {}, message: {}'.format(e, channel, message))
