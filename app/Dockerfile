FROM python:3.6

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=datafeed/main.py

ADD ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

ADD . /code

WORKDIR /code

CMD ["flask", "run", "--host=0.0.0.0"]
