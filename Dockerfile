FROM ubuntu

RUN apt-get update
RUN apt-get install python3 python3-pip python3-lxml -y
RUN apt-get install libxslt1-dev -y

COPY * /home/
WORKDIR /home/

RUN pip3 install -r requirements.txt
RUN cat slack_env >> ~/.bashrc

CMD python3 bot.py
