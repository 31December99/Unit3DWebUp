FROM python:3.12-slim AS base
WORKDIR /app

COPY *.py /app/
COPY config/ /app/config/
COPY external/ /app/external/
COPY models/ /app/models/
COPY repositories/ /app/repositories/
COPY services/ /app/services/
COPY use_case/ /app/use_case/
COPY requirements.txt /app/

# Install requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Flutter
FROM nginx:alpine AS frontend
COPY UI/build/web/ /usr/share/nginx/html
COPY UI/nginx/default.conf /etc/nginx/conf.d/default.conf

FROM python:3.12-slim
WORKDIR /app

# Installa webserver for flutter app
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

COPY --from=base /app /app

# Copy the builded web folder /build/web and nginx configuration
COPY --from=frontend /usr/share/nginx/html /usr/share/nginx/html
COPY --from=frontend /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

# Start
CMD python /app/start.py & nginx -g 'daemon off;'
