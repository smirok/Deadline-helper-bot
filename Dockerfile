FROM python:3.8-slim-buster

RUN mkdir /data
WORKDIR /data
COPY requirements.txt /data
RUN pip install -r requirements.txt
COPY . /data

ENTRYPOINT ["python3", "main.py"]
