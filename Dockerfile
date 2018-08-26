FROM python:3.7

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=datahub/main.py

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY . /code

WORKDIR /code

CMD ["flask", "run", "--host=0.0.0.0"]
