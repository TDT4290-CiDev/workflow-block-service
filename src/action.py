class Action:
    def __init__(self, function):
        self.function = function
        pass

class DummyAction(Action):

    def act(self, *args):
        print('Performing action on %s'.format(str(k)))

class UpdateAction(Action):

    def act(self, arg):
        return self.function(arg)