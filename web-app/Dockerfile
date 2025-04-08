FROM python:3.10-slim

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --ignore-pipfile

COPY . .

RUN pipenv install pylint black

CMD ["pipenv", "run", "pylint", "app.py"]
