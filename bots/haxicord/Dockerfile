FROM haxe:3.4.7-buster

RUN apt update;apt install bash git g++ -y
RUN haxelib install haxicord
RUN haxelib install hxcpp
RUN mkdir -p /app/src /app/bin
COPY build.hxml /app/build.hxml
COPY Main.hx /app/src/Main.hx
RUN cd app;haxe build.hxml