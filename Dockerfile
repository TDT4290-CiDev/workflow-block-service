FROM python:3.7-alpine

RUN adduser -D cidev
WORKDIR /home/cidev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY src src
COPY boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP src/main.py

RUN chown -R cidev:cidev ./
USER cidev

# Echo the host IP address. This is used in development to send mail to a local fake SMTP server.
RUN echo $(ip route show | awk '/default/ {print $3}')

EXPOSE 8080
ENTRYPOINT ["./boot.sh"]
