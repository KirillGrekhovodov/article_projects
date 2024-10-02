FROM python:3.12.7-slim-bookworm
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
COPY source/ /code
EXPOSE 8000