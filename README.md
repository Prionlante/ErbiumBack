# Erbium back-end #
> Note: `The project step in a deep development stage`

> Note: `The database changes some times, so the development version may fail to get news sources`

This repository stores part of the backend of "Voice of City" project. 
This project was mainly developed to demonstrate the possible functionality of the project for various competitions and a potential sponsor.

At the moment, the project has the following functionality:
* Chat bot system (this repository)
* Recommendatiom system (this repository)
* Data Base interaction
* News parser

# How to start app? #
## Custom ##
You can run each microservice separately, but you must install the required python modules. This method suitable if you want to change the code and see how it will work with the changes.

## Docker ###
If you are using docker, then you need to run compose file in the root directory of the project with the command:
```sh
docker compose up
```
[![Docker hub page]https://hub.docker.com/r/serg228/vs)](https://hub.docker.com/r/serg228/vs)

# How to use? #
Once you have launched the application, go to
```sh
http://0.0.0.0:80/
```
You can freely navigate on the sections of the site, studying and testing functionality
