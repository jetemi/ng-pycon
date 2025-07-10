#!/bin/bash

echo "🚀 Setting up PyCon Nigeria development environment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update the .env file with your configuration!"
fi

echo "📦 Installing Node.js dependencies..."
npm install

echo "🎨 Building initial CSS..."
npm run build-css-prod

echo "🐳 Starting Docker services..."
docker-compose up -d db

echo "⏳ Waiting for database to be ready..."
sleep 10

echo "🐍 Installing Python dependencies and running migrations..."
docker-compose run --rm web python manage.py migrate

echo "👤 Creating superuser..."
docker-compose run --rm web python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

echo "🌟 Starting all services..."
docker-compose --profile dev up

echo "✅ Development environment is ready!"
echo "📋 Access the application at: http://localhost:8000"
echo "🔧 Admin panel: http://localhost:8000/admin" 