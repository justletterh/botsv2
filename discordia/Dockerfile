FROM debian:stable-slim

RUN apt update
RUN apt install -y curl
RUN cd /;curl -L https://github.com/luvit/lit/raw/master/get-lit.sh | sh
RUN mv /lit /bin/lit;mv /luvit /bin/luvit;mv /luvi /bin/luvi
RUN cd /;: `lit install SinisterRectus/discordia||exit 0`