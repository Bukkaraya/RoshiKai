# RoshiKai
A bot for slack.

The bot can be deployed with Docker.

Docker commands to run bot

Todo:
- [ ] Add a Jenkins job to automatically deploy the bot

```
docker build -t roshikai:latest .
docker run --rm roshikai:latest 
```

The docker build commands requires a slack_env file.
A sample for the file is provided below.

---
```
export SLACK_BOT_TOKEN=<your_slack_token_here>
python3 bot.py
```
