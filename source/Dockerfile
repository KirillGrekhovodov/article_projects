FROM python:3.12.7-slim-bookworm
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt update
RUN apt install gettext -y
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
COPY source/ /code
EXPOSE 8000

#apt install gettext