FROM node:latest AS build-stage
LABEL maintainer="william.wernert@securityonionsolutions.com"

RUN mkdir -p /app
WORKDIR /app

COPY package*.json ./
RUN npm install --loglevel warn

COPY . .
RUN npm run build --modern

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 4242


