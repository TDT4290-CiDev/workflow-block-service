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

* Send requests by navigating to localhost:8080/<...> in ypur favorite browser or with curl.

* Send POST requests using curl:
```bash
curl -H "Content-type: application/json" \
     -X POST localhost:8080/example \
          -d '{"params": {"param1": "ex1", "param2":1}}'
          ```
