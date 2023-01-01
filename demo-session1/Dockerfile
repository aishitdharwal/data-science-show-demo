FROM python:3.7.3-alpine

# working directory
WORKDIR /demo-session1

# copy source code to working directory
COPY . /demo-session1

# install apt-get
RUN apt-get update

# install packages from requirements.txt
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

CMD ["echo", "hello world"]