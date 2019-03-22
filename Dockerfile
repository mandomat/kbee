FROM alpine:latest

WORKDIR /usr/src/app

RUN apk update && apk add python3 py3-pip py3-greenlet py3-gevent && rm -f /var/cache/apk/*
RUN adduser -h /usr/src/app/ -D -H pyuser

COPY requirements.txt ./
RUN cat requirements.txt | grep -vE "greenlet|gevent|psycopg2-binary" > requirements2.txt && pip3 install -r requirements2.txt
COPY . .

RUN chown -R pyuser:pyuser /usr/src/app

EXPOSE 8080

USER pyuser:pyuser
