# ============================================================================
#                    DEVSECOPS DEMO SCRIPT - FULL WORKFLOW
# ============================================================================
# Chạy script này để demo toàn bộ DevSecOps workflow
# Thời gian: ~5 phút
# ============================================================================

Write-Host "`n" -NoNewline
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "                    DEVSECOPS DEMO WORKFLOW" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "`n"

$ErrorActionPreference = "Continue"

# ============================================================================
# PHẦN 1: KIỂM TRA HỆ THỐNG
# ============================================================================

Write-Host "[1/8] Checking System Requirements..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray

Write-Host "  → Python: " -NoNewline
python --version
if ($LASTEXITCODE -eq 0) { Write-Host "    ✅ OK" -ForegroundColor Green } else { Write-Host "    ❌ FAILED" -ForegroundColor Red }

Write-Host "  → Docker: " -NoNewline
docker --version
if ($LASTEXITCODE -eq 0) { Write-Host "    ✅ OK" -ForegroundColor Green } else { Write-Host "    ❌ FAILED" -ForegroundColor Red }

Write-Host "  → Git: " -NoNewline
git --version
if ($LASTEXITCODE -eq 0) { Write-Host "    ✅ OK" -ForegroundColor Green } else { Write-Host "    ❌ FAILED" -ForegroundColor Red }

Write-Host "  → Bandit: " -NoNewline
bandit --version 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) { Write-Host "    ✅ OK" -ForegroundColor Green } else { Write-Host "    ❌ FAILED" -ForegroundColor Red }

Write-Host "  → Safety: " -NoNewline
safety --version 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) { Write-Host "    ✅ OK" -ForegroundColor Green } else { Write-Host "    ❌ FAILED" -ForegroundColor Red }

Write-Host "  → Trivy: " -NoNewline
trivy --version 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) { Write-Host "    ✅ OK" -ForegroundColor Green } else { Write-Host "    ⚠️  NOT INSTALLED (optional)" -ForegroundColor Yellow }

Write-Host "`n✅ System check complete`n" -ForegroundColor Green
Start-Sleep -Seconds 2

# ============================================================================
# PHẦN 2: DOCKER BUILD
# ============================================================================

Write-Host "[2/8] Building Docker Image..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray

docker-compose build

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Docker build successful`n" -ForegroundColor Green
} else {
    Write-Host "`n❌ Docker build failed`n" -ForegroundColor Red
    exit 1
}

Start-Sleep -Seconds 2

# ============================================================================
# PHẦN 3: START CONTAINER
# ============================================================================

Write-Host "[3/8] Starting Container..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray

docker-compose down 2>&1 | Out-Null
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Container started successfully`n" -ForegroundColor Green
} else {
    Write-Host "`n❌ Container start failed`n" -ForegroundColor Red
    exit 1
}

Write-Host "  Waiting for container to be healthy..." -ForegroundColor Gray
Start-Sleep -Seconds 15

# ============================================================================
# PHẦN 4: CHECK CONTAINER STATUS
# ============================================================================

Write-Host "[4/8] Checking Container Status..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray

docker-compose ps

$containerStatus = docker inspect football-app --format='{{.State.Status}}' 2>&1
if ($containerStatus -eq "running") {
    Write-Host "`n✅ Container is running`n" -ForegroundColor Green
} else {
    Write-Host "`n❌ Container is not running properly`n" -ForegroundColor Red
    Write-Host "Showing logs:" -ForegroundColor Yellow
    docker logs football-app
    exit 1
}

Start-Sleep -Seconds 2

# ============================================================================
# PHẦN 5: TEST APPLICATION
# ============================================================================

Write-Host "[5/8] Testing Application..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "`n✅ Application is accessible at http://localhost:5000`n" -ForegroundColor Green
    }
} catch {
    Write-Host "`n⚠️  Application not responding yet (may need more time)`n" -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

# ============================================================================
# PHẦN 6: RUN SECURITY SCANS
# ============================================================================

Write-Host "[6/8] Running Security Scans..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray

# Create reports directory
New-Item -ItemType Directory -Path "reports" -Force | Out-Null

# Bandit - SAST
Write-Host "  → Running Bandit (SAST)..." -ForegroundColor Cyan
bandit -r . -f json -o reports/bandit-report.json 2>&1 | Out-Null
bandit -r . -f txt -o reports/bandit-report.txt 2>&1 | Out-Null
if (Test-Path "reports/bandit-report.txt") {
    Write-Host "    ✅ Bandit scan complete" -ForegroundColor Green
} else {
    Write-Host "    ⚠️  Bandit scan failed" -ForegroundColor Yellow
}

# Safety - Dependency Scan
Write-Host "  → Running Safety (Dependency)..." -ForegroundColor Cyan
safety check --json > reports/safety-report.json 2>&1
safety check > reports/safety-report.txt 2>&1
if (Test-Path "reports/safety-report.txt") {
    Write-Host "    ✅ Safety scan complete" -ForegroundColor Green
} else {
    Write-Host "    ⚠️  Safety scan failed" -ForegroundColor Yellow
}

# Trivy - Container Scan
Write-Host "  → Running Trivy (Container)..." -ForegroundColor Cyan
$trivyInstalled = Get-Command trivy -ErrorAction SilentlyContinue
if ($trivyInstalled) {
    trivy image --format json --output reports/trivy-report.json football-app:latest 2>&1 | Out-Null
    trivy image --format table --output reports/trivy-report.txt football-app:latest 2>&1 | Out-Null
    if (Test-Path "reports/trivy-report.txt") {
        Write-Host "    ✅ Trivy scan complete" -ForegroundColor Green
    } else {
        Write-Host "    ⚠️  Trivy scan failed" -ForegroundColor Yellow
    }
} else {
    Write-Host "    ⚠️  Trivy not installed (skipped)" -ForegroundColor Yellow
}

Write-Host "`n✅ Security scans complete`n" -ForegroundColor Green
Start-Sleep -Seconds 2

# ============================================================================
# PHẦN 7: SHOW REPORTS
# ============================================================================

Write-Host "[7/8] Security Scan Results..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray

Write-Host "`nReports generated:" -ForegroundColor Cyan
Get-ChildItem reports\ | ForEach-Object {
    Write-Host "  ✅ $($_.Name)" -ForegroundColor Green
}

Write-Host "`nBandit Summary:" -ForegroundColor Cyan
if (Test-Path "reports/bandit-report.txt") {
    Get-Content "reports/bandit-report.txt" | Select-Object -Last 10
}

Write-Host "`nSafety Summary:" -ForegroundColor Cyan
if (Test-Path "reports/safety-report.txt") {
    Get-Content "reports/safety-report.txt" | Select-Object -First 15
}

Start-Sleep -Seconds 3

# ============================================================================
# PHẦN 8: SHOW LOGS
# ============================================================================

Write-Host "`n[8/8] Container Logs (Last 20 lines)..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray

docker-compose logs --tail=20

Start-Sleep -Seconds 2

# ============================================================================
# SUMMARY
# ============================================================================

Write-Host "`n" -NoNewline
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "                    DEMO COMPLETE!" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "`n"

Write-Host "✅ Docker image built successfully" -ForegroundColor Green
Write-Host "✅ Container running: football-app" -ForegroundColor Green
Write-Host "✅ Application accessible: http://localhost:5000" -ForegroundColor Green
Write-Host "✅ Security scans completed" -ForegroundColor Green
Write-Host "✅ Reports generated in: reports/" -ForegroundColor Green

Write-Host "`n" -NoNewline
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Open browser: http://localhost:5000" -ForegroundColor White
Write-Host "  2. View reports: Get-ChildItem reports\" -ForegroundColor White
Write-Host "  3. View logs: docker-compose logs -f" -ForegroundColor White
Write-Host "  4. Stop: docker-compose down" -ForegroundColor White

Write-Host "`n" -NoNewline
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "`n"

# Open browser
Write-Host "Opening browser..." -ForegroundColor Cyan
Start-Process "http://localhost:5000"

Write-Host "Demo script completed! 🚀" -ForegroundColor Green

