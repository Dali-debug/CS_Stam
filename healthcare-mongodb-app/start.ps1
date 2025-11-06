# Healthcare MongoDB FastAPI - Quick Start Script
# Run this script to set up and start the application

Write-Host "Healthcare MongoDB FastAPI - Quick Start" -ForegroundColor Green
Write-Host "==================================================`n"

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "ERROR: Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Create virtual environment if it does not exist
if (-not (Test-Path "venv")) {
    Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "`nVirtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Create .env if it does not exist
if (-not (Test-Path ".env")) {
    Write-Host "`nCreating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ".env file created" -ForegroundColor Green
    Write-Host "WARNING: Please update MongoDB connection string in .env file" -ForegroundColor Yellow
} else {
    Write-Host "`n.env file already exists" -ForegroundColor Green
}

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "`nLogs directory created" -ForegroundColor Green
}

# Display next steps
Write-Host "`n==================================================`n" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your MongoDB connection string"
Write-Host "2. Start the server with: uvicorn app.main:app --reload"
Write-Host "3. Visit: http://localhost:8000/docs for API documentation"
Write-Host "`nOptional:"
Write-Host "- Seed sample data: python -m app.scripts.seed_data"
Write-Host "- Test database: python -m app.scripts.test_database"
Write-Host "`n==================================================`n"

# Ask if user wants to start server
$response = Read-Host "Start development server now? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "`nStarting FastAPI server..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop the server`n" -ForegroundColor Yellow
    uvicorn app.main:app --reload --port 8000
} else {
    Write-Host "`nRun uvicorn app.main:app --reload when ready!" -ForegroundColor Cyan
}
