class Deadline:
    def __init__(self, remain_day, work, channel, worker):
        self.remain_day = remain_day
        self.work = work
        self.channel = channel
        self.worker = worker

    def __str__(self):
        return 'remain_day: {}, work: {}, channel: {}, worker: {}'.format(self.remain_day, self.work, self.channel, self.worker)
