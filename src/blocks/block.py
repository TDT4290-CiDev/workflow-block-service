

class WorkflowBlock:

    def get_info(self):
        """
        Returns a dictionary specifying behaviour of the block, as well as input parameters and outputs.
        """
        pass

    def execute(self, params):
        """
        Implements the functionality of the block. Called by the server upon requests to the block's endpoint.
        """
        pass
