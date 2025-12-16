#!/bin/bash

# PitchOS Deployment Script
set -e

echo "🚀 PitchOS Deployment Script"
echo "=============================="

# Configuration
ENVIRONMENT=${1:-development}
BUILD_FRONTEND=${BUILD_FRONTEND:-true}
BUILD_BACKEND=${BUILD_BACKEND:-true}
PUSH_IMAGES=${PUSH_IMAGES:-false}
REGISTRY=${REGISTRY:-""}

echo "Environment: $ENVIRONMENT"
echo "Build Frontend: $BUILD_FRONTEND"
echo "Build Backend: $BUILD_BACKEND"
echo "Push Images: $PUSH_IMAGES"

# Check prerequisites
check_prerequisites() {
    echo "🔍 Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed"
        exit 1
    fi
    
    if [ ! -f ".env" ]; then
        echo "⚠️  .env file not found, creating from template..."
        cp .env.example .env
        echo "📝 Please edit .env file with your configuration"
    fi
    
    echo "✅ Prerequisites check passed"
}

# Build images
build_images() {
    echo "🔨 Building Docker images..."
    
    if [ "$BUILD_BACKEND" = true ]; then
        echo "Building backend image..."
        docker build -f Dockerfile.backend -t pitchos-backend:latest .
        
        if [ "$PUSH_IMAGES" = true ] && [ -n "$REGISTRY" ]; then
            docker tag pitchos-backend:latest $REGISTRY/pitchos-backend:latest
            docker push $REGISTRY/pitchos-backend:latest
        fi
    fi
    
    if [ "$BUILD_FRONTEND" = true ]; then
        echo "Building frontend image..."
        docker build -f Dockerfile.frontend -t pitchos-frontend:latest .
        
        if [ "$PUSH_IMAGES" = true ] && [ -n "$REGISTRY" ]; then
            docker tag pitchos-frontend:latest $REGISTRY/pitchos-frontend:latest
            docker push $REGISTRY/pitchos-frontend:latest
        fi
    fi
    
    echo "✅ Images built successfully"
}

# Deploy services
deploy_services() {
    echo "🚀 Deploying services..."
    
    case $ENVIRONMENT in
        "development")
            docker-compose up -d
            ;;
        "production")
            docker-compose --profile production up -d
            ;;
        "staging")
            docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
            ;;
        *)
            echo "❌ Unknown environment: $ENVIRONMENT"
            exit 1
            ;;
    esac
    
    echo "✅ Services deployed"
}

# Health check
health_check() {
    echo "🏥 Performing health checks..."
    
    # Wait for services to start
    sleep 10
    
    # Check backend
    if curl -f http://localhost:8000/ > /dev/null 2>&1; then
        echo "✅ Backend is healthy"
    else
        echo "❌ Backend health check failed"
        docker-compose logs backend
        exit 1
    fi
    
    # Check frontend
    if curl -f http://localhost:3000/ > /dev/null 2>&1; then
        echo "✅ Frontend is healthy"
    else
        echo "❌ Frontend health check failed"
        docker-compose logs frontend
        exit 1
    fi
    
    echo "✅ All services are healthy"
}

# Show status
show_status() {
    echo "📊 Service Status:"
    docker-compose ps
    
    echo ""
    echo "🌐 Access Points:"
    echo "- Frontend: http://localhost:3000"
    echo "- Backend API: http://localhost:8000"
    echo "- API Docs: http://localhost:8000/docs"
    
    if [ "$ENVIRONMENT" = "production" ]; then
        echo "- Production: http://localhost (via Nginx)"
    fi
}

# Cleanup function
cleanup() {
    echo "🧹 Cleaning up..."
    docker system prune -f
    echo "✅ Cleanup completed"
}

# Main execution
main() {
    check_prerequisites
    
    if [ "$1" = "cleanup" ]; then
        cleanup
        exit 0
    fi
    
    if [ "$1" = "down" ]; then
        echo "🛑 Stopping services..."
        docker-compose down
        exit 0
    fi
    
    build_images
    deploy_services
    health_check
    show_status
    
    echo ""
    echo "🎉 Deployment completed successfully!"
    echo "📝 Logs: docker-compose logs -f"
    echo "🛑 Stop: ./deploy.sh down"
    echo "🧹 Cleanup: ./deploy.sh cleanup"
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy"|"development"|"production"|"staging")
        main "$@"
        ;;
    "down")
        docker-compose down
        ;;
    "cleanup")
        cleanup
        ;;
    "logs")
        docker-compose logs -f "${2:-}"
        ;;
    "restart")
        docker-compose restart "${2:-}"
        ;;
    "build")
        build_images
        ;;
    *)
        echo "Usage: $0 [deploy|development|production|staging|down|cleanup|logs|restart|build]"
        echo ""
        echo "Commands:"
        echo "  deploy       - Deploy in development mode (default)"
        echo "  development  - Deploy in development mode"
        echo "  production   - Deploy in production mode with Nginx"
        echo "  staging      - Deploy in staging mode"
        echo "  down         - Stop all services"
        echo "  cleanup      - Clean up Docker resources"
        echo "  logs [service] - Show logs for all services or specific service"
        echo "  restart [service] - Restart all services or specific service"
        echo "  build        - Build Docker images only"
        echo ""
        echo "Environment variables:"
        echo "  BUILD_FRONTEND=true|false - Build frontend image (default: true)"
        echo "  BUILD_BACKEND=true|false  - Build backend image (default: true)"
        echo "  PUSH_IMAGES=true|false    - Push images to registry (default: false)"
        echo "  REGISTRY=registry-url     - Docker registry URL"
        exit 1
        ;;
esac
