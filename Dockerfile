FROM ubuntu:24.04
# 우분투 24.04 기반의 커스텀 이미지 생성

# Custom image based on Linux base image + basic runtime features
ENV APP_PORT=8080
ENV APP_MESSAGE="Hello from Codyssey custom image"

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash codyssey
WORKDIR /home/codyssey/app
COPY app /home/codyssey/app
RUN chown -R codyssey:codyssey /home/codyssey/app
USER codyssey

EXPOSE ${APP_PORT}
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${APP_PORT}/ || exit 1

CMD ["python3", "/home/codyssey/app/server.py"]
