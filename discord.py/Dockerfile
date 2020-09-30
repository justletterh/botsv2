FROM python:3.8-alpine

RUN apk add --no-cache build-base libffi-dev
RUN pip install -U discord.py[voice] jishaku psutil
RUN apk add bash