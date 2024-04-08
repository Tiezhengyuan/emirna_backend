FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y iputils.ping

# source code in /web in the container
WORKDIR /code
# install dependency
COPY requirements.txt /code/
RUN pip install -r requirements.txt
# copy all source code into /code/
COPY . /code/