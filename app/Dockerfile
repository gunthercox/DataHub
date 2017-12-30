FROM python:3.6

EXPOSE 5000

ENV FLASK_APP=main.py

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]
