FROM ubuntu

RUN apt-get update
RUN apt-get install python3 python3-pip -y

COPY * /home/
WORKDIR /home/

RUN pip3 install -r requirements.txt

ENV SLACK_BOT_TOKEN xoxb-315965117873-527939551655-6S7zOp5TXTHkcvvoopI5QMiC

CMD python3 bot.py
