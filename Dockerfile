FROM python:3.8-slim
LABEL version=2.2021
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
CMD gunicorn alyticstest.wsgi:application --bind 0.0.0.0:8000
