# ===========================================================================
#                    DEPLOY TO HEROKU - SIMPLE SCRIPT
# ===========================================================================
# This script deploys the Football app to Heroku cloud platform
# ===========================================================================

Write-Host "`n========================================================================" -ForegroundColor Cyan
Write-Host "                    DEPLOY TO HEROKU CLOUD" -ForegroundColor Cyan
Write-Host "========================================================================`n" -ForegroundColor Cyan

# Check if Heroku CLI is installed
Write-Host "[1/8] Checking Heroku CLI..." -ForegroundColor Yellow
if (-not (Get-Command heroku -ErrorAction SilentlyContinue)) {
    Write-Host "  ERROR: Heroku CLI not found!`n" -ForegroundColor Red
    Write-Host "  Install Heroku CLI:" -ForegroundColor Yellow
    Write-Host "  1. Download: https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Cyan
    Write-Host "  2. Or use Chocolatey: choco install heroku-cli -y`n" -ForegroundColor Cyan
    exit 1
}
Write-Host "  Heroku CLI installed`n" -ForegroundColor Green

# Login to Heroku
Write-Host "[2/8] Logging in to Heroku..." -ForegroundColor Yellow
Write-Host "  Browser will open for authentication...`n" -ForegroundColor Gray

heroku auth:whoami 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Please login..." -ForegroundColor Cyan
    heroku login
}

$herokuUser = heroku auth:whoami 2>&1
Write-Host "  Logged in as: $herokuUser`n" -ForegroundColor Green

# Create Heroku app
Write-Host "[3/8] Creating Heroku app..." -ForegroundColor Yellow
$appName = "football-app-$(Get-Random -Maximum 9999)"
Write-Host "  App name: $appName" -ForegroundColor Cyan

heroku create $appName 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  App created successfully`n" -ForegroundColor Green
} else {
    Write-Host "  App creation failed (may already exist)`n" -ForegroundColor Yellow
}

# Add Heroku remote
Write-Host "[4/8] Adding Heroku remote..." -ForegroundColor Yellow
git remote remove heroku 2>&1 | Out-Null
heroku git:remote -a $appName 2>&1 | Out-Null
Write-Host "  Remote added`n" -ForegroundColor Green

# Set environment variables
Write-Host "[5/8] Setting environment variables..." -ForegroundColor Yellow

if (Test-Path ".env") {
    $envContent = Get-Content ".env"
    $secretKey = ($envContent | Select-String "SECRET_KEY=(.+)").Matches.Groups[1].Value
    
    if ($secretKey) {
        heroku config:set SECRET_KEY=$secretKey -a $appName 2>&1 | Out-Null
        Write-Host "  SECRET_KEY configured" -ForegroundColor Green
    }
}

heroku config:set FLASK_ENV=production -a $appName 2>&1 | Out-Null
Write-Host "  FLASK_ENV=production`n" -ForegroundColor Green

# Deploy to Heroku
Write-Host "[6/8] Deploying to Heroku..." -ForegroundColor Yellow
Write-Host "  This may take 3-5 minutes...`n" -ForegroundColor Gray

# Get current branch
$currentBranch = git branch --show-current 2>&1

Write-Host "  Pushing $currentBranch to Heroku..." -ForegroundColor Cyan
git push heroku ${currentBranch}:main 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n  Deployment successful!`n" -ForegroundColor Green
} else {
    Write-Host "`n  Deployment failed! Check errors above.`n" -ForegroundColor Red
    exit 1
}

# Scale dynos
Write-Host "[7/8] Scaling dynos..." -ForegroundColor Yellow
heroku ps:scale web=1 -a $appName 2>&1 | Out-Null
Write-Host "  Web dyno scaled to 1`n" -ForegroundColor Green

# Get app info
Write-Host "[8/8] Getting app information..." -ForegroundColor Yellow

$appInfo = heroku apps:info -a $appName 2>&1
$appUrl = ($appInfo | Select-String "Web URL:\s+(.+)").Matches.Groups[1].Value.Trim()

Write-Host "`n========================================================================" -ForegroundColor Cyan
Write-Host "                    DEPLOYMENT COMPLETE!" -ForegroundColor Cyan
Write-Host "========================================================================`n" -ForegroundColor Cyan

Write-Host "App Name: $appName" -ForegroundColor Green
Write-Host "App URL: $appUrl" -ForegroundColor Green
Write-Host "Heroku User: $herokuUser`n" -ForegroundColor Green

Write-Host "Useful Commands:" -ForegroundColor Yellow
Write-Host "  View logs: heroku logs --tail -a $appName" -ForegroundColor White
Write-Host "  Open app: heroku open -a $appName" -ForegroundColor White
Write-Host "  Restart: heroku restart -a $appName" -ForegroundColor White
Write-Host "  Status: heroku ps -a $appName`n" -ForegroundColor White

Write-Host "Opening app in browser...`n" -ForegroundColor Cyan
heroku open -a $appName

Write-Host "========================================================================`n" -ForegroundColor Cyan

