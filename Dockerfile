FROM python:3.11
RUN apt-get update && apt-get install -y netcat-traditional vim
MAINTAINER TiezhengYuan

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code
WORKDIR /code

RUN /usr/local/bin/python -m pip install --upgrade pip
ADD ./requirements.txt /code/
RUN pip install -r requirements.txt
ADD . ./code/