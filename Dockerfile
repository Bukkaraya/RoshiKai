FROM ubuntu

RUN apt-get update
RUN apt-get install python3 python3-pip -y
RUN apt-get install libxslt1-dev -y

COPY * /home/
WORKDIR /home/

RUN slack_env
RUN pip3 install -r requirements.txt

CMD python3 bot.py
