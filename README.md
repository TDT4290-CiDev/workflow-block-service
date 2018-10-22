# WorkflowBlockService

## Run and debug Docker container in PyCharm
NOTE: Make sure you are using PyCharm 2017 Professional Edition
* Build the docker image using 
```bash
docker image -t <your-image-name> .
```
Note the dot at the end: this notifies docker that the Dockerfile at the current directory should be used to build the image.

* Check out this guide https://blog.jetbrains.com/pycharm/2017/03/docker-compose-getting-flask-up-and-running/, especially the section on 'Setting up PyCharm'. Follow this guide to set a Docker image as the project interpreter. Use the Docker option instead of docker-compose, and choose the image you created in the previous step.



* In the Run configurations options screen, make sure the local port is exposed. The 'Docker container settings' field should include `-p 8080:8080` or whatever your desired ports are.

* Run the app using the normal Run and Debug buttons in PyCharm!

* Send requests by navigating to localhost:8080/<...> in your favorite browser or with curl.

* Send POST requests using curl:
```bash
curl -H "Content-type: application/json" \
     -X POST localhost:8080/example \
          -d '{"params": {"param1": "ex1", "param2":1}}'
```

## Adding new blocks
Blocks are implemented as classes with the following structure:

```python
from blocks.block import WorkflowBlock


class MyWorkflowBlock(WorkflowBlock):
    
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
    
    def resume(self, state, params):
        """
        Resumes execution of a suspended block.
        :param state: The state dictionary returned by the block upon suspension.
        :param params: Any new parameters given upon resumption.
        """
        pass
```

The result of the `get_info` method is returned by the `/<block>/info` endpoint, and provides other services with
information about the block. In particular, it allows the workflow designer to know how to represent the block, what
kind of parameters it needs, and what kind of data it returns. The dictionary has the following structure:

```python
{
    'description': 'Description of the block.',
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
            'type': 'float',
            'description': 'The first output.'
        },
        'output2': {
            'type': 'boolean',
            'description': 'The second output.'
        }
    },
    
    # Define whether the block can suspend execution and wait for external interaction.
    'can_suspend_execution': False
}
```

The `execute` method implements the functionality of the blocks; possibly with the help of any optional helper functions.
`params` will be passed as a dictionary containing the parameter values provided by the user. All values specified in
the info dictionary can be assumed to be present, and with the correct type, as this is checked by the server.
The method must return a dictionary containing the output values specified by the info dictionary.

## Suspending execution
Sometimes, a workflow block may need to suspend execution in order to wait for user input or another external event.
This is done by returning the result of the `suspend` method (inherited from `WorkflowBlock`). A state dictionary must 
passed to the method when suspending. This dictionary should include all parameters need to resume execution,
including information about at what point the execution was suspended, and any parameters originally passed passed to 
the `execute` function that are required upon resuming. This could be as simple as passing the original `params`
dictionary, or more complex. If additional parameters should be provided by the user upon resuming execution, these
should be requested by passing a dictionary as the `requested_params` argument. This has the same format as the `params`
item in the block information dictionary.

Upon resumption, the resume method of the block will be called. This method takes two parameters: `state`, which is the
same dictionary as given to the `suspend` method, and `params`, which contains any new parameters. The `resume` method
can itself suspend execution, in which case `state` must contain any info required to distinguish between different
suspensions. The returned result should be equivalent to the one usually returned by execute. See below for a simple
example. 

```python
def execute(self, params):
    # ... Initial code here ...
    if need_additional_data:
        requested_params = {
            'new_param': {
                'type': 'string',
                'description': 'A new parameter that we did not originally request.'
            }
        }
        return self.suspend(params, requested_params)
    return result

def resume(self, state, params):
    # ... Resume execution ....
    return result
```