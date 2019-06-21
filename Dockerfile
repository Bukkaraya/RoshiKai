FROM ubuntu

RUN apt-get update
RUN apt-get install python3 python3-pip python3-dev python3-lxml -y
RUN apt-get install libxslt1-dev -y

COPY * /app/
WORKDIR /app
RUN apt-get install libffi-dev && \
        pip3 install -r requirements.txt
RUN chmod +x bot.py slack_env
ENV DEBUG=False

CMD ["/bin/bash", "slack_env"]
