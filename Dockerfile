FROM nginx:alpine
LABEL maintainer="rye6837"
ENV APP_ENV=development
COPY app/ /usr/share/nginx/html/
EXPOSE 80