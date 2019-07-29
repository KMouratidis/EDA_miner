# our base image
FROM python:3.6-onbuild

# Get the necessary dependencies for pygraphviz
RUN apt-get update
RUN apt-get install gcc libgraphviz-dev graphviz -y --fix-missing

# copy files required for the app to run
COPY ./ /usr/src/app/

# tell the port number the container should expose
EXPOSE 8050

# run the application
WORKDIR /usr/src/app/EDA_miner
CMD ["python3", "app.py"]
