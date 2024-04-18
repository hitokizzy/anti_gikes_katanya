FROM python:3.10

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

#set a default command

CMD bash start