# our base image
FROM amd64/ubuntu

# Get the necessary dependencies for pygraphviz
RUN apt-get update
RUN apt-get install gcc libgraphviz-dev graphviz -y --fix-missing

# Get pip3
RUN apt-get install python3-pip python3-dev -y

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/

# RUN conda uninstall sympy
RUN pip3 install -r /usr/src/app/requirements.txt

# copy files required for the app to run
COPY ./ /usr/src/app/

# tell the port number the container should expose
EXPOSE 8050

# run the application
WORKDIR /usr/src/app/EDA_miner
CMD ["python3", "app.py"]
