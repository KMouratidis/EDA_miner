# our base image
FROM python:3.6-onbuild

# copy files required for the app to run
COPY ./ /usr/src/app/

# run the application
WORKDIR /usr/src/app/

CMD ["gunicorn", "-b", "127.0.0.1:5000","app:app"]
