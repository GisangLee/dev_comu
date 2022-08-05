FROM python:3.9

ENV PYTHONUNBUFFERED 1
RUN apt-get -y update && apt-get clean

WORKDIR /usr/src/dev_comu

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000