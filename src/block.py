class Block:

    def __init__(self, name):
        self.name = name
        self.activated = False
        self.output = {}

    def execute(self, **kwargs):
        # Dummy block
        self.input = kwargs
        self.activated = True
        print(self.name + ' is executing!')


class ForEachBlock(Block):

    def __init__(self, name, action):
        self.action = action
        super().__init__(name)

    def execute(self, **kwargs):
        self.input = kwargs.items()
        self.output = {}
        self.activated=True
        for k, v in kwargs.items():
            self.output[k] = self.action.act(v)
        return self.output

