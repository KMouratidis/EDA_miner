<img src="https://github.com/KMouratidis/EDA_miner_public/blob/master/EDA_miner/static/images/y3d.png" width="250" align="left">

# EDA_miner

<badges> <img src="https://img.shields.io/badge/doc--coverage-78%25-brightgreen.svg"> <img src="https://img.shields.io/badge/code--coverage-63%25-green.svg"> <img src="https://img.shields.io/badge/tests-100%25-brightgreen.svg"> <a href="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg"></a> <img src="https://img.shields.io/badge/docker%20build-passing-brightgreen.svg">  [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted%20(modified)-ff69b4.svg)](CODE_OF_CONDUCT.md)  </badges>
<a href="https://lgtm.com/projects/g/KMouratidis/EDA_miner_public/context:javascript"><img alt="Language grade: JavaScript" src="https://img.shields.io/lgtm/grade/javascript/g/KMouratidis/EDA_miner_public.svg?logo=lgtm&logoWidth=18"/></a>
<a href="https://lgtm.com/projects/g/KMouratidis/EDA_miner_public/context:python"><img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/KMouratidis/EDA_miner_public.svg?logo=lgtm&logoWidth=18"/></a>
<a href="https://codeclimate.com/github/KMouratidis/EDA_miner_public/maintainability"><img src="https://api.codeclimate.com/v1/badges/63c6e2c44862a35e148e/maintainability" height=20 /></a>

A visualization and analytics dashboard that is able to connect to APIs, receive your data,
and allow you to run Machine Learning models from a server. Started as a university project, and will be deployed in their servers probably later this year.
Also being worked on together with university staff for an E.U.-sponsored project.


Want to contribute? Take a moment to review the [style and contributor guidelines](https://github.com/KMouratidis/EDA_miner_public/wiki/Style-guide-and-contributor-guidelines)

Want to chat? Join us on <a href="https://join.slack.com/t/edaminer/shared_invite/enQtNzA5MDc1MTE3NDk0LTJmNGYyYTY4NDAwMGJkYTI5NDg2NzAyOWQ2OTcxYTU0NTc4NzEwMWQ0ZjAwYWFkYmUyYjJmZWFkZjM3OWZkYmY"><img src="https://img.shields.io/badge/chat-slack-blueviolet.svg"></a>

Just looking around? Then you can either install locally or with docker.

#### Locally:
1. Get Python3.6+, optionally with Anaconda. You might want to set up a [virtual environment](https://stackoverflow.com/questions/41972261/what-is-a-virtualenv-and-why-should-i-use-one)
2. Download (either via `git clone https://github.com/KMouratidis/EDA_miner_public` or as a zip)
3. You'll need [redis](https://redis.io) (if on Windows, you might also need [this](https://github.com/dmajkic/redis/downloads)) and [graphviz](https://www.graphviz.org/) (for pygraphviz)
4. Run `pip install -r requirements.txt`.
5. Navigate to the `/EDA_miner` folder.
6. Create a `.env` file with your credentials, according to the given template.
7. Run `python users_mgt.py` to create a dummy database and user (u: admin, pw: admin)
8. Run the app, e.g. with gunicorn: `gunicorn wsgi:application`.
9. If you want to work with Google Analytics:
    - Navigate to `/EDA_miner/google_analytics`.
    - Start the app with either:
      - Run `pip install -r requirements.txt` and `python app.py`
    or
      - `sudo docker build --rm -t kmouratidis/ganalytics .` and `sudo docker run --rm --network host kmouratidis/ganalytics`
10. Go to your browser, `http://127.0.0.1:8000/`.

#### Docker:
1. Download (either via `git clone https://github.com/KMouratidis/EDA_miner_public` or as a zip)
2. Get Redis in Docker, start a server, and publish port 6379, by running: `sudo docker run --name=redis-devel --publish=6379:6379 --hostname=redis --restart=on-failure --detach redis:latest`
3. Navigate to the EDA Miner folder and run this to build the docker container: `sudo docker build -t kmouratidis/eda_miner .`
4. Run the app container: `sudo docker run --network host kmouratidis/eda_miner`
5. If you want to work with Google Analytics:
  - Navigate to `/EDA_miner/google_analytics`.
  - Run `sudo docker build --rm -t kmouratidis/ganalytics .` and `sudo docker run --rm --network host kmouratidis/ganalytics`
6. Go to http://127.0.0.1:8000/.
<br>

### Example of Model Builder

![Interface options 1](https://raw.githubusercontent.com/KMouratidis/EDA_miner_public/master/images/screenshots/ModelBuilder.png)

### Example of the Schema Inference Tab:

![Interface options 2](https://raw.githubusercontent.com/KMouratidis/EDA_miner_public/master/images/screenshots/Datatype_Inference.png)

### Example of the Explore & Visualize Tab:

![Interface options 3](https://raw.githubusercontent.com/KMouratidis/EDA_miner_public/master/images/screenshots/GraphMaker.png)

### Example of the Analyze & Predict Tab:

![Interface options 4](https://raw.githubusercontent.com/KMouratidis/EDA_miner_public/master/images/screenshots/FittingModels.png)

### Example of the Connecting to an API:

![Interface options 5](https://raw.githubusercontent.com/KMouratidis/EDA_miner_public/master/images/screenshots/API_connect.png)

### Example of PDF report generation
![Interface options 6](https://raw.githubusercontent.com/KMouratidis/EDA_miner_public/master/images/screenshots/PDF_Reports.png)

### Example of previewing data:

![Interface options 7](https://raw.githubusercontent.com/KMouratidis/EDA_miner_public/master/images/screenshots/Preview_Data.png)
