from blocks.block import WorkflowBlock


class Example(WorkflowBlock):

    def get_info(self):
        return {
            'description': 'An example block used for documentation.',
            'params': {
                'param1': {
                    'type': 'string',
                    'description': 'The first parameter.'
                },
                'param2': {
                    'type': 'integer',
                    'description': 'The second parameter.'
                }
            },
            'outputs': {
                'output1': {
                    'type': 'string',
                    'description': 'The first output.'
                },
                'output2': {
                    'type': 'string',
                    'description': 'The second output.'
                }
            },
            'can_suspend_execution': False
        }

    def execute(self, params):
        if params['param1'] == 'suspend':
            return self.suspend({'params': params, 'suspend_count': 1},
                                {'param1': {'type': 'string', 'description': 'The first parameter.'}})

        return {
            'output1': 'Hello',
            'output2': 'world!'
        }

    def resume(self, state, params):
        suspend_count = state['suspend_count'] + 1

        if params['param1'] == 'suspend':
            return self.suspend({'params': params, 'suspend_count': suspend_count},
                                {'param1': {'type': 'string', 'description': 'The first parameter.'}})

        return {
            'output1': 'Hello',
            'output2': 'world!'
        }
