FROM python:3.10-slim

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv
RUN pipenv lock
RUN pipenv install --deploy --ignore-pipfile

ENV PIPENV_VENV_IN_PROJECT=1
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

EXPOSE 5000

CMD ["pipenv", "run", "python", "app.py"]
