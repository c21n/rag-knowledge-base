# RAG Knowledge Base - Setup Script for Windows
# This script automates the initial deployment setup

Write-Host "🚀 RAG Knowledge Base - Setup Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Check prerequisites
Write-Host ""
Write-Host "Checking prerequisites..."

# Check Docker
$dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerInstalled) {
    Write-Host "✗ Docker is not installed" -ForegroundColor Red
    Write-Host "  Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
}
Write-Host "✓ Docker installed" -ForegroundColor Green

# Check Docker Compose
$composeInstalled = Get-Command docker-compose -ErrorAction SilentlyContinue
if (-not $composeInstalled) {
    Write-Host "✗ Docker Compose is not installed" -ForegroundColor Red
    Write-Host "  Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
}
Write-Host "✓ Docker Compose installed" -ForegroundColor Green

# Create .env file if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host ""
    Write-Host "Creating .env file from template..."
    Copy-Item .env.example .env
    Write-Host "✓ .env file created" -ForegroundColor Green
    Write-Host "⚠ Please edit .env and add your API keys" -ForegroundColor Yellow
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

# Create data directories
Write-Host ""
Write-Host "Creating data directories..."
New-Item -ItemType Directory -Force -Path "data\chromadb" | Out-Null
New-Item -ItemType Directory -Force -Path "data\uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "data\sqlite" | Out-Null
Write-Host "✓ Data directories created" -ForegroundColor Green

# Validate required environment variables
Write-Host ""
Write-Host "Validating environment configuration..."

if (Test-Path .env) {
    $envContent = Get-Content .env -Raw
    
    # Check for API keys
    if ($envContent -match "OPENAI_API_KEY=your_openai_api_key" -or $envContent -match "OPENAI_API_KEY=`$") {
        Write-Host "⚠ OPENAI_API_KEY not configured" -ForegroundColor Yellow
        Write-Host "  Please set OPENAI_API_KEY in .env file"
    } else {
        Write-Host "✓ OPENAI_API_KEY configured" -ForegroundColor Green
    }
    
    if ($envContent -match "API_KEY=your_alibaba_bailian" -or $envContent -match "API_KEY=`$") {
        Write-Host "⚠ API_KEY (Alibaba Bailian) not configured" -ForegroundColor Yellow
        Write-Host "  Please set API_KEY in .env file"
    } else {
        Write-Host "✓ API_KEY configured" -ForegroundColor Green
    }
}

# Check Docker daemon
Write-Host ""
Write-Host "Checking Docker daemon..."
try {
    $dockerInfo = docker info 2>&1
    Write-Host "✓ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker daemon is not running" -ForegroundColor Red
    Write-Host "  Please start Docker Desktop and try again"
    exit 1
}

# Build images
Write-Host ""
Write-Host "Building Docker images..."
Write-Host "This may take a few minutes..."
docker-compose build --no-cache
Write-Host "✓ Docker images built" -ForegroundColor Green

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "✓ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start the application:"
Write-Host "   docker-compose up -d"
Write-Host ""
Write-Host "2. View logs:"
Write-Host "   docker-compose logs -f"
Write-Host ""
Write-Host "3. Stop the application:"
Write-Host "   docker-compose down"
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost"
Write-Host "   API Docs: http://localhost:8000/docs"
Write-Host "   API Base: http://localhost:8000"
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
