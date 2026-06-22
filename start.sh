#!/bin/bash

# Quant Risk Engine Startup Script
# This script starts the entire quant risk management system

set -e

echo "🚀 Starting Quant Risk Engine..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if required directories exist
echo "📁 Checking project structure..."
if [ ! -d "java-engine" ] || [ ! -d "python-analytics" ] || [ ! -d "web-ui" ]; then
    echo "❌ Missing required directories. Please ensure you're in the project root."
    exit 1
fi

# Create logs directory
mkdir -p logs

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🏥 Checking service health..."

# Check Java Risk Engine
if curl -f http://localhost:8080/actuator/health > /dev/null 2>&1; then
    echo "✅ Java Risk Engine is running on http://localhost:8080"
else
    echo "⚠️  Java Risk Engine may still be starting..."
fi

# Check Python Analytics API
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Python Analytics API is running on http://localhost:8000"
else
    echo "⚠️  Python Analytics API may still be starting..."
fi

# Check Web UI
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Web UI is running on http://localhost:3000"
else
    echo "⚠️  Web UI may still be starting..."
fi

# Check Airflow
if curl -f http://localhost:8081 > /dev/null 2>&1; then
    echo "✅ Airflow is running on http://localhost:8081"
else
    echo "⚠️  Airflow may still be starting..."
fi

# Check Grafana
if curl -f http://localhost:3001 > /dev/null 2>&1; then
    echo "✅ Grafana is running on http://localhost:3001"
else
    echo "⚠️  Grafana may still be starting..."
fi

echo ""
echo "🎉 Quant Risk Engine is starting up!"
echo ""
echo "📊 Access Points:"
echo "   • Web UI: http://localhost:3000"
echo "   • Risk Engine API: http://localhost:8080"
echo "   • Analytics API: http://localhost:8000"
echo "   • Airflow: http://localhost:8081"
echo "   • Grafana: http://localhost:3001"
echo "   • Prometheus: http://localhost:9090"
echo ""
echo "📋 Useful Commands:"
echo "   • View logs: docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Restart services: docker-compose restart"
echo "   • Update services: docker-compose up -d --build"
echo ""
echo "🔧 Configuration:"
echo "   • Edit docker-compose.yml to modify service settings"
echo "   • Update IB credentials in docker-compose.yml"
echo "   • Check logs/ directory for application logs"
echo ""

# Show running containers
echo "🐳 Running containers:"
docker-compose ps
