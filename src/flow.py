from enum import Enum


class FlowStatus(Enum):
    COMPLETED, IN_PROGRESS, WAITING, CANCELED, ERROR = range(5)


class Flow:

    def __init__(self, name, description, trigger, steps, **kwargs):
        self.name = name
        self.description = description
        self.steps = steps
        self.trigger = trigger
        self.trigger.add_flow(self)
        self.status = FlowStatus.WAITING
        self.input = kwargs
        self.output = {}


    def set_trigger(self, trigger):
        self.trigger = trigger

    def perform_actions(self):
        self.status = FlowStatus.IN_PROGRESS
        output = self.input
        for s in self.steps:
            output = s.execute(**output)
        self.output = output
        self.status = FlowStatus.COMPLETED






