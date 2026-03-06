#!/bin/bash
# RAG Knowledge Base - Setup Script for Linux/Mac
# This script automates the initial deployment setup

set -e

echo "🚀 RAG Knowledge Base - Setup Script"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check prerequisites
echo ""
echo "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed${NC}"
    echo "  Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✓ Docker installed${NC}"

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose is not installed${NC}"
    echo "  Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}⚠ Please edit .env and add your API keys${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Create data directories
echo ""
echo "Creating data directories..."
mkdir -p data/chromadb
mkdir -p data/uploads
mkdir -p data/sqlite
echo -e "${GREEN}✓ Data directories created${NC}"

# Validate required environment variables
echo ""
echo "Validating environment configuration..."

if [ -f .env ]; then
    # Check for API keys
    if grep -q "OPENAI_API_KEY=your_openai_api_key" .env || grep -q "OPENAI_API_KEY=$" .env; then
        echo -e "${YELLOW}⚠ OPENAI_API_KEY not configured${NC}"
        echo "  Please set OPENAI_API_KEY in .env file"
    else
        echo -e "${GREEN}✓ OPENAI_API_KEY configured${NC}"
    fi
    
    if grep -q "API_KEY=your_alibaba_bailian" .env || grep -q "API_KEY=$" .env; then
        echo -e "${YELLOW}⚠ API_KEY (Alibaba Bailian) not configured${NC}"
        echo "  Please set API_KEY in .env file"
    else
        echo -e "${GREEN}✓ API_KEY configured${NC}"
    fi
fi

# Check Docker daemon
echo ""
echo "Checking Docker daemon..."
if docker info &> /dev/null; then
    echo -e "${GREEN}✓ Docker daemon is running${NC}"
else
    echo -e "${RED}✗ Docker daemon is not running${NC}"
    echo "  Please start Docker and try again"
    exit 1
fi

# Build images
echo ""
echo "Building Docker images..."
echo "This may take a few minutes..."
docker-compose build --no-cache
echo -e "${GREEN}✓ Docker images built${NC}"

echo ""
echo "====================================="
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo -e "${CYAN}Next steps:${NC}"
echo ""
echo "1. Start the application:"
echo "   docker-compose up -d"
echo ""
echo "2. View logs:"
echo "   docker-compose logs -f"
echo ""
echo "3. Stop the application:"
echo "   docker-compose down"
echo ""
echo -e "${CYAN}Access the application:${NC}"
echo "   Frontend: http://localhost"
echo "   API Docs: http://localhost:8000/docs"
echo "   API Base: http://localhost:8000"
echo ""
echo "====================================="
