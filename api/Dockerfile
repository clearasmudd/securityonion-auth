FROM python:alpine
LABEL maintainer="william.wernert@securityonionsolutions.com"

ARG SECRET_KEY
ARG SSL_CERT
ARG SSL_KEY

ENV SECRET_KEY="${SECRET_KEY}"
ENV REFRESH_TOKEN_TIMEOUT="30"
ENV TOKEN_TIMEOUT="60"
ENV DB_URI="sqlite:///db.sqlite"


COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

EXPOSE 5000
ENTRYPOINT [ "gunicorn", "--certfile", "${SSL_CERT}", "--keyfile", "${SSL_KEY}", "-w", "2", "-b", "0.0.0.0:5000", "api:app" ]
