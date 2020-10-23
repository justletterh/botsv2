FROM alpine:latest

RUN apk add nodejs-current npm build-base git libtool autoconf automake python2

RUN git clone --single-branch --branch master https://github.com/justletterh/Tupperbox.git /app 

WORKDIR /app
RUN npm i

ENTRYPOINT ["/usr/bin/node"]