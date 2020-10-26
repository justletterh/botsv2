FROM node:current-buster

RUN apt update;apt install -y git
RUN git clone https://github.com/justletterh/rainy.git /app
RUN cd /app;dir -aux
RUN cd /app;npm install eris axios chrono-node eris minimist node-vibrant pg ytdl-core