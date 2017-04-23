from config import SLACK_BOT_TOKEN
from datetime import datetime, timedelta
from logger import logger
from sheet.deadline import Deadline
from slacker import Slacker
from typing import List


class Bot:
    def __init__(self, debug=False):
        self.__slacker = Slacker(SLACK_BOT_TOKEN)
        self.__debug = debug

    def post_message(self, deadlines: List[Deadline]):
        self.__delete_older_messages()

        for deadline in deadlines:
            if 0 < deadline.remain_day <= 1:
                self.__post_message(deadline.channel, deadline.worker, deadline.remain_day, deadline.work)
            elif deadline.remain_day == 0:
                self.__post_message(deadline.channel, deadline.worker, deadline.remain_day, deadline.work)
            elif deadline.remain_day < 0:
                self.__post_message(deadline.channel, deadline.worker, deadline.remain_day, deadline.work)

    def __delete_older_messages(self):
        bot = self.__slacker.users.get_user_id('kronos')

        result = self.__slacker.channels.list()
        for channel in result.body['channels']:
            channel_id = channel['id']
            yesterday = datetime.today() - timedelta(days=1)
            history = self.__slacker.channels.history(channel_id, latest=yesterday.timestamp(), count=10)
            for message in history.body['messages']:
                if 'user' in message and message['user'] == bot:
                    try:
                        self.__slacker.chat.delete(channel_id, message['ts'])
                    except Exception as e:
                        logger.warn(e)

    def __post_message(self, channel, worker, remain_day, work):
        try:
            message = self.__generate_message(worker, remain_day, work)

            full_channel = self.__get_full_channel(channel)
            self.__slacker.chat.post_message(full_channel, message, as_user=True, link_names=1)
        except Exception as e:
            logger.warn('error: {}, channel: {}, message: {}'.format(e, channel, message))

    def __generate_message(self, worker, remain_day, work):
        message = '{} 입니다 : {}'.format(self.__get_remain_day_str(remain_day), work)

        if datetime.today().weekday() <= 4:
            message = '{} 님 {}'.format(worker, message)

        return message

    def __get_remain_day_str(self, remain_day: int):
        if remain_day == 0:
            return 'D-DAY'
        elif remain_day < 0:
            return 'D + {}일'.format(-remain_day)
        else:
            return 'D - {}일'.format(remain_day)

    def __get_full_channel(self, channel):
        if self.__debug is False:
            return '#' + channel
        else:
            return '#bot_test'
