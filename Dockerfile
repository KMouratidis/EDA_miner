# our base image
FROM continuumio/anaconda3

# Get the necessary dependencies for pygraphviz
RUN apt-get update
RUN apt-get install gcc libgraphviz-dev graphviz -y --fix-missing

# Get graphviz
RUN conda install python-graphviz

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
# Uninstall sympy because updating it throws a distutils error
RUN conda uninstall sympy
RUN pip install -r /usr/src/app/requirements.txt

# copy files required for the app to run
COPY ./ /usr/src/app/

# tell the port number the container should expose
EXPOSE 8050

# run the application
WORKDIR /usr/src/app/EDA_miner
CMD ["python", "app.py"]
