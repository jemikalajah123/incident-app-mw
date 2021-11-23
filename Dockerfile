# pull official base image
FROM python:3.9.5-alpine

# set work directory
WORKDIR /incidentapp

# set environment variables
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /incidentapp/
RUN pip install -r requirements.txt

# copy project
COPY . /incidentapp/

#set environment vars to be used
ENV AUTHOR="Philip"

#port from the container to expose to host
EXPOSE 8000

#Tell image what to do when it starts as a container
CMD python manage.py migrate