# Multi-stage build for frontend assets
FROM node:18-alpine AS frontend-builder

# Set working directory for frontend build
WORKDIR /app

# Copy package files for frontend dependencies
COPY package*.json ./

# Install Node.js dependencies
RUN npm ci --only=production

# Copy source files needed for frontend build
COPY tailwind.config.js ./
COPY pyconng/static/css/src ./pyconng/static/css/src
COPY pyconng/static/js ./pyconng/static/js
COPY pyconng/templates ./pyconng/templates
COPY pyconng/apps ./pyconng/apps
COPY home/templates ./home/templates
COPY search/templates ./search/templates

# Build Tailwind CSS
RUN npm run build

# Main Python application stage
FROM python:3.12-slim-bookworm

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses PostgreSQL, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Copy built frontend assets from the frontend-builder stage
COPY --from=frontend-builder --chown=wagtail:wagtail /app/pyconng/static/css/pyconng.css ./pyconng/static/css/
COPY --from=frontend-builder --chown=wagtail:wagtail /app/node_modules/alpinejs/dist/cdn.min.js ./pyconng/static/js/alpine.min.js

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
CMD set -xe; python manage.py migrate --noinput; gunicorn pyconng.wsgi:application
