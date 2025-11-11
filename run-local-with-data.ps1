# ===========================================================================
#                   RUN LOCAL WITH DATA POPULATION
# ===========================================================================
# This script:
# 1. Removes old database
# 2. Populates database with football data from API
# 3. Runs Flask app locally
# ===========================================================================

Write-Host "`n=========================================" -ForegroundColor Green
Write-Host "🚀 STARTING LOCAL FOOTBALL APP WITH DATA" -ForegroundColor Green
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

# Step 3: Run Flask app
Write-Host "`n🌐 Starting Flask app on http://localhost:5000..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Green

$env:FLASK_ENV = "development"
$env:FLASK_APP = "app.py"
python app.py

