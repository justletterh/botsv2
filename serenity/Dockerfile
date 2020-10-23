FROM rust:buster
ARG HID
ARG DISCORD_TOKEN
ENV HID=$HID
ENV DISCORD_TOKEN=$DISCORD_TOKEN

RUN apt update;apt full-upgrade -y
RUN mkdir -p /app/src
COPY Cargo.toml /app/Cargo.toml
COPY serenity.rs.rs /app/src/main.rs
RUN cd app;cargo build