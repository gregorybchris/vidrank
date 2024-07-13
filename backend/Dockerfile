FROM python:3.12-slim

COPY . /app
WORKDIR /app
RUN pip install poetry
RUN poetry install --no-dev
EXPOSE 8000
CMD LOG_LEVEL=DEBUG poetry run fastapi run vidrank/app/app.py --reload