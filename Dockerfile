FROM ubuntu

RUN apt-get update
RUN apt-get install python3 python3-pip python3-dev python3-lxml -y
RUN apt-get install libxslt1-dev -y

COPY * /home/
WORKDIR /home/
RUN apt-get install libffi-dev
RUN pip3 install -r requirements.txt

CMD /bin/bash slack_env
