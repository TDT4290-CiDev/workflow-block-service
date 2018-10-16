

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

    def suspend(self, state):
        """
        Creates a suspend response, signalling that the block will wait for further input before resuming.
        :param state: A dictionary containing all information the block will need to resume execution when called again.
        :return: A tuple (state, status), where status will be 'suspend', to signal that the block is suspending.
        """

        return state, 'suspend'

    def resume(self, state, params):
        """
        Resumes execution of a suspended block.
        :param state: The state dictionary returned by the block upon suspension.
        :param params: Any new parameters given upon resumption.
        """
        pass