# our base image
FROM continuumio/anaconda3

# Get the necessary dependencies for pygraphviz
RUN apt-get update
RUN apt-get install gcc libgraphviz-dev graphviz -y --fix-missing

# Get graphviz
RUN conda install python-graphviz

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt

# copy files required for the app to run
COPY ./* /usr/src/app/
COPY apps /usr/src/app/apps
COPY assets /usr/src/app/assets
COPY docs /usr/src/app/docs
COPY images /usr/src/app/images
COPY static /usr/src/app/static


# tell the port number the container should expose
EXPOSE 8050

# run the application
WORKDIR /usr/src/app 
CMD ["python", "app.py"]
