# our base image
FROM python:3.6-onbuild

# copy files required for the app to run
COPY ./ /usr/src/app/

# run the application
WORKDIR /usr/src/app/
CMD ["python3", "app.py"]
