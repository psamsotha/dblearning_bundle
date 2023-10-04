FROM python:3.11-slim-buster

WORKDIR /home/dblearning_bundle

COPY ./requirements-test.txt ./requirements-test.txt

RUN pip install --upgrade pip \
    && pip install -r requirements-test.txt

COPY . /home/dblearning_bundle/

CMD ["pytest"]
