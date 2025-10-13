# ===========================================================================
#                   RUN DOCKER WITH DATA POPULATION
# ===========================================================================
# This script:
# 1. Removes old database
# 2. Populates database with football data from API
# 3. Builds and runs Docker container
# ===========================================================================

Write-Host "`n=========================================" -ForegroundColor Green
Write-Host "🐳 STARTING DOCKER WITH DATA" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Step 1: Remove old database
Write-Host "`n📁 Removing old database..." -ForegroundColor Yellow
if (Test-Path "footballinfor.db") {
    Remove-Item "footballinfor.db" -Force
    Write-Host "  ✅ Old database removed" -ForegroundColor Green
} else {
    Write-Host "  ℹ️  No old database found" -ForegroundColor Cyan
}

# Step 2: Populate database
Write-Host "`n📊 Populating database with football data..." -ForegroundColor Yellow
python populate_db.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Failed to populate database!" -ForegroundColor Red
    exit 1
}

# Step 3: Stop existing containers
Write-Host "`n🛑 Stopping existing containers..." -ForegroundColor Yellow
docker-compose down

# Step 4: Build and run Docker
Write-Host "`n🔨 Building Docker image..." -ForegroundColor Yellow
docker-compose build

Write-Host "`n🚀 Starting Docker container..." -ForegroundColor Yellow
docker-compose up -d

# Step 5: Show logs
Write-Host "`n📋 Container logs:" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Green
Start-Sleep -Seconds 3
docker-compose logs

Write-Host "`n=========================================" -ForegroundColor Green
Write-Host "✅ Docker container is running!" -ForegroundColor Green
Write-Host "🌐 Access app at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Green
Write-Host "`nUseful commands:" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f    # Follow logs" -ForegroundColor Cyan
Write-Host "  docker-compose down       # Stop container" -ForegroundColor Cyan
Write-Host "  docker-compose restart    # Restart container" -ForegroundColor Cyan

