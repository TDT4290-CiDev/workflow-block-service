import datetime
from threading import Timer, Event

class Trigger:
    flows = []

    def add_flow(self, flow):
        self.flows.append(flow)

    def trigger(self):
        for f in self.flows:
            f. perform_actions()

class ScheduledTrigger(Trigger):

    def __init__(self, time, repeat_interval=None, until=None):
        now = datetime.datetime.now()
        if time < now:
            print('Error: cant set up a timed event for a time in the past.')
            return
        time_until_trigger = time - now
        t = Timer(time_until_trigger, self.trigger)
        t.start()
        self.repeat_interval = repeat_interval
        self.until = until

    def trigger(self):
        if self.repeat_interval is not None:
            time_until_trigger = self.repeat_interval
            if datetime.datetime.now() + self.repeat_interval <= until:
                t = Timer(time_until_trigger, self.trigger)
                t.start()
        super().trigger()



