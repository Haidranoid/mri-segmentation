## Build docker image

- docker build -t flask-app:local .
- docker build --no-cache -t flask-app:final .
- docker build -t pipeline-app .

## Run a docker container from the image built

- docker run --rm -p 5000:5000 flask-app:local
- docker run --rm -p 5000:5000 flask-app:final
- docker run --rm -v $(pwd)/input:/input -v $(pwd)/output:/output pipeline-app
