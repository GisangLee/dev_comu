FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get -y install vim && apt-get clean
RUN mkdir /dev_comu
RUN mkdir /dev_comu/src

WORKDIR /dev_comu/src
ADD . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /dev_comu/src

CMD ["python", "manage.py", "makemigrations", "python", "manage.py", "migrate", "python", "manage.py", "runserver", "0.0.0.0:8000"]