FROM python:3.8-slim-buster

# working directory
WORKDIR /demo-session

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install pip

# install packages from requirements.txt
RUN pip install --upgrade pip

COPY . .

CMD ["echo", "hello world"]