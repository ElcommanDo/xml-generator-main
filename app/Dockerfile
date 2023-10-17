# FROM python:alpine
# FROM python:3.9-alpine3.16
FROM nickgryg/alpine-pandas

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev \
    libffi-dev openssl-dev

RUN pip3 install --upgrade pip

EXPOSE 5000

WORKDIR /app

COPY * /app/

RUN pip3 install -r requirements.txt

CMD python3 app.py