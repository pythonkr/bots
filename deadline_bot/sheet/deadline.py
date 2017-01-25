class Deadline:
    def __init__(self, remain_day, work, channel):
        self.remain_day = remain_day
        self.work = work
        self.channel = channel

    def __str__(self):
        return 'remain_day: {}, work: {}, channel: {}'.format(self.remain_day, self.work, self.channel)

