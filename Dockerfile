FROM python:3.7-alpine

RUN adduser -D cidev
WORKDIR /home/cidev

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY code code
COPY boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP code/main.py

RUN chown -R cidev:cidev ./
USER cidev

EXPOSE 8080
ENTRYPOINT ["./boot.sh"]
