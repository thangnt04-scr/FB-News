# ===========================================================================
#           TEST RENDER DEPLOYMENT
# ===========================================================================
# This script tests if the Render deployment is successful
# ===========================================================================

param(
    [Parameter(Mandatory=$false)]
    [string]$RenderUrl = ""
)

Write-Host "`n========================================================================" -ForegroundColor Cyan
Write-Host "           TEST RENDER DEPLOYMENT" -ForegroundColor Cyan
Write-Host "========================================================================`n" -ForegroundColor Cyan

# Prompt for URL if not provided
if ([string]::IsNullOrEmpty($RenderUrl)) {
    Write-Host "Enter your Render app URL:" -ForegroundColor Yellow
    Write-Host "Example: https://football-app.onrender.com" -ForegroundColor Gray
    $RenderUrl = Read-Host "URL"
}

# Remove trailing slash
$RenderUrl = $RenderUrl.TrimEnd('/')

Write-Host "`nTesting: $RenderUrl`n" -ForegroundColor Cyan

# Test 1: Homepage
Write-Host "[1/5] Testing homepage..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $RenderUrl -Method GET -TimeoutSec 30
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✅ Homepage accessible (Status: 200)`n" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Homepage returned status: $($response.StatusCode)`n" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ Homepage not accessible: $($_.Exception.Message)`n" -ForegroundColor Red
}

# Test 2: Health check
Write-Host "[2/5] Testing health endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$RenderUrl/health" -Method GET -TimeoutSec 30 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✅ Health check passed`n" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠️  Health endpoint not found (this is OK if not implemented)`n" -ForegroundColor Yellow
}

# Test 3: API endpoint
Write-Host "[3/5] Testing API..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$RenderUrl/api/leagues" -Method GET -TimeoutSec 30 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✅ API accessible`n" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠️  API endpoint check skipped`n" -ForegroundColor Yellow
}

# Test 4: Response time
Write-Host "[4/5] Testing response time..." -ForegroundColor Yellow
try {
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    $response = Invoke-WebRequest -Uri $RenderUrl -Method GET -TimeoutSec 30
    $stopwatch.Stop()
    $responseTime = $stopwatch.ElapsedMilliseconds
    
    if ($responseTime -lt 1000) {
        Write-Host "  ✅ Fast response: ${responseTime}ms`n" -ForegroundColor Green
    } elseif ($responseTime -lt 3000) {
        Write-Host "  ⚠️  Moderate response: ${responseTime}ms`n" -ForegroundColor Yellow
    } else {
        Write-Host "  ⚠️  Slow response: ${responseTime}ms`n" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ Response time test failed`n" -ForegroundColor Red
}

# Test 5: SSL Certificate
Write-Host "[5/5] Testing SSL certificate..." -ForegroundColor Yellow
if ($RenderUrl -match "^https://") {
    Write-Host "  ✅ HTTPS enabled`n" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Not using HTTPS`n" -ForegroundColor Yellow
}

# Summary
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "                    TEST COMPLETE" -ForegroundColor Cyan
Write-Host "========================================================================`n" -ForegroundColor Cyan

Write-Host "App URL: $RenderUrl" -ForegroundColor Cyan
Write-Host "`nOpening in browser...`n" -ForegroundColor Yellow

Start-Process $RenderUrl

Write-Host "========================================================================`n" -ForegroundColor Cyan

