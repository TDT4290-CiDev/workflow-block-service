from blocks.block import WorkflowBlock


class Approval(WorkflowBlock):

    def get_info(self):
        return {
            'description': 'Block used when any kind of approval is required for the continued execution.',
            'params': {
                'description': {
                    'type': 'string',
                    'description': 'Description of the kind of approval that is requested.'
                },
            },
            'outputs': {
            },
            'can_suspend_execution': True
        }

    def execute(self, params):
        return self.suspend({'description': params['description']})

    def resume(self, state, params):
        return {}
