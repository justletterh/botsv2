FROM debian:stable

RUN apt update;apt full-upgrade -y
RUN apt install curl git gcc -y
RUN curl https://nim-lang.org/choosenim/init.sh -sSf | bash -s -- -y
RUN echo "export PATH=/root/.nimble/bin:$PATH">>~/.profile
ENV PATH=/root/.nimble/bin:$PATH
RUN nimble install dimscord@#head -y