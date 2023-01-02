FROM python:3.8-slim-buster

# Copy the current dir to dir in the image
COPY . /demo_session

# Set working dir
WORKDIR /demo_session

# install packages from requirements.txt
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

CMD ["python3", "main.py"]