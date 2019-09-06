FROM node:lts-alpine
LABEL maintainer="william.wernert@securityonionsolutions.com"

ARG SSL_CERT
ARG SSL_KEY
ARG API_URL
ARG API_PORT="5000"

ENV API_URL="https://l${API_URL}:${API_URL}"

RUN npm install -g http-server

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build --modern

EXPOSE 8080
ENTRYPOINT [ "http-server", "-ssl", "--cert", "${SSL_CERT}", "--key", "${SSL_KEY}", "--cors", "dist" ]
