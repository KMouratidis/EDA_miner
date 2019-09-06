<img src="https://github.com/KMouratidis/EDA_miner/blob/master/EDA_miner/static/images/y3d.png" width="250" align="left">

# EDA_miner

<badges> <img src="https://img.shields.io/badge/doc--coverage-72%25-green.svg"> <img src="https://img.shields.io/badge/code--coverage-63%25-green.svg"> <img src="https://img.shields.io/badge/tests-100%25-brightgreen.svg"> <a href="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg"></a> <img src="https://img.shields.io/badge/docker%20build-passing-brightgreen.svg">  [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted%20(modified)-ff69b4.svg)](CODE_OF_CONDUCT.md)  </badges>
<a href="https://lgtm.com/projects/g/KMouratidis/EDA_miner/context:javascript"><img alt="Language grade: JavaScript" src="https://img.shields.io/lgtm/grade/javascript/g/KMouratidis/EDA_miner.svg?logo=lgtm&logoWidth=18"/></a>
<a href="https://lgtm.com/projects/g/KMouratidis/EDA_miner/context:python"><img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/KMouratidis/EDA_miner.svg?logo=lgtm&logoWidth=18"/></a>
<a href="https://codeclimate.com/github/KMouratidis/EDA_miner/maintainability"><img src="https://api.codeclimate.com/v1/badges/63c6e2c44862a35e148e/maintainability" height=20 /></a>
[![Build Status](https://travis-ci.com/KMouratidis/EDA_miner.svg?branch=master)](https://travis-ci.com/KMouratidis/EDA_miner)

A visualization and analytics dashboard that is able to connect to APIs, receive your data,
and allow you to run Machine Learning models from a server. Started as a university project, and will be deployed in their servers probably later this year.
Also being worked on together with university staff for an E.U.-sponsored project.


Want to contribute? Take a moment to review the [style and contributor guidelines](https://github.com/KMouratidis/EDA_miner/wiki/Style-guide-and-contributor-guidelines)

Want to chat? Join us on <a href="https://join.slack.com/t/edaminer/shared_invite/enQtNzA5MDc1MTE3NDk0LTJmNGYyYTY4NDAwMGJkYTI5NDg2NzAyOWQ2OTcxYTU0NTc4NzEwMWQ0ZjAwYWFkYmUyYjJmZWFkZjM3OWZkYmY"><img src="https://img.shields.io/badge/chat-slack-blueviolet.svg"></a>

Just looking around? Then you can either install locally or with docker.

#### Locally:
1. Get Python3.6+, optionally with Anaconda. You might want to set up a [virtual environment](https://stackoverflow.com/questions/41972261/what-is-a-virtualenv-and-why-should-i-use-one)
2. Download (either via `git clone https://github.com/KMouratidis/EDA_miner` or as a zip)
3. You'll need [redis](https://redis.io) (if on Windows, you might also need [this](https://github.com/dmajkic/redis/downloads)) and [graphviz](https://www.graphviz.org/) (for pygraphviz)
4. Run `pip install -r requirements.txt`.
5. Navigate to the `/EDA_miner` folder.
6. Create an `env.py` file with your credentials, according to the given template (`env_template.py`) or simply rename it (some functionality will not work).
7. Run `python initialize_project.py` to create a dummy database and user (u: admin, pw: admin)
8. Run the app, e.g. with gunicorn: `gunicorn wsgi:application`.
9. If you want to work with Google Analytics:
    - Navigate to `/EDA_miner/google_analytics`.
    - Start the app with either:
      - Run `pip install -r requirements.txt` and `python app.py`
    or
      - `sudo docker build --rm -t kmouratidis/ganalytics .` and `sudo docker run --rm --network host kmouratidis/ganalytics`
10. Go to your browser, `http://127.0.0.1:8000/`.

#### Docker:
1. Download (either via `git clone https://github.com/KMouratidis/EDA_miner` or as a zip)
2. Get Redis in Docker, start a server, and publish port 6379, by running: `sudo docker run --rm --name=redis-devel --publish=6379:6379 --hostname=redis --restart=on-failure --detach redis:latest`
3. Navigate to the EDA Miner folder and run this to build the docker container: `sudo docker build --rm -t kmouratidis/eda_miner .`
4. Run the app container: `sudo docker run --rm --network host kmouratidis/eda_miner`
5. If you want to work with Google Analytics:
    - Navigate to `/EDA_miner/google_analytics`.
    - Run `sudo docker build --rm -t kmouratidis/ganalytics .` and `sudo docker run --rm --network host kmouratidis/ganalytics`
6. Go to `http://127.0.0.1:8000/`.
<br>

### Examples of the Modeling app

![Interface options 1](https://raw.githubusercontent.com/KMouratidis/EDA_miner/master/images/screenshots/ModelBuilder.png)
![Interface options 2](https://raw.githubusercontent.com/KMouratidis/EDA_miner/master/images/screenshots/FittingModels1.png)
![Interface options 3](https://raw.githubusercontent.com/KMouratidis/EDA_miner/master/images/screenshots/FittingModels2.png)

### Examples of the Visualization app:

![Interface options 4](https://raw.githubusercontent.com/KMouratidis/EDA_miner/master/images/screenshots/ChartMaker.png)
![Interface options 5](https://raw.githubusercontent.com/KMouratidis/EDA_miner/master/images/screenshots/Mapping.png)

### Examples of the Data app:

![Interface options 6](https://raw.githubusercontent.com/KMouratidis/EDA_miner/master/images/screenshots/Upload.png)
![Interface options 7](https://raw.githubusercontent.com/KMouratidis/EDA_miner/master/images/screenshots/API_connect.png)
![Interface options 8](https://raw.githubusercontent.com/KMouratidis/EDA_miner/master/images/screenshots/Datatype_Inference.png)
![Interface options 9](https://raw.githubusercontent.com/KMouratidis/EDA_miner/master/images/screenshots/Preview_Data.png)
