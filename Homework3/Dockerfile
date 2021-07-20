FROM python:3.9

WORKDIR /app

COPY . /app

RUN pipenv install --system --deploy

CMD ['python', 'core.py']