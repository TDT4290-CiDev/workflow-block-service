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
        return {
            'output1': 'Hello',
            'output2': 'world!'
        }
