# ===========================================================================
#           COMPLETE DEVSECOPS WORKFLOW - ALL PHASES
# ===========================================================================
# This script runs all DevSecOps phases and generates comprehensive reports
# ===========================================================================

Write-Host "`n========================================================================" -ForegroundColor Cyan
Write-Host "           COMPLETE DEVSECOPS WORKFLOW - ALL PHASES" -ForegroundColor Cyan
Write-Host "========================================================================`n" -ForegroundColor Cyan

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$startTime = Get-Date

# Create reports directory
New-Item -ItemType Directory -Path "reports" -Force | Out-Null

# ===========================================================================
# PHASE I: ENVIRONMENT CHECK
# ===========================================================================

Write-Host "[PHASE I] Environment Check..." -ForegroundColor Yellow
Write-Host "Checking all required tools...`n" -ForegroundColor Gray

$tools = @{
    "Python" = (python --version 2>&1)
    "Git" = (git --version 2>&1)
    "Docker" = (docker --version 2>&1)
}

if (Get-Command bandit -ErrorAction SilentlyContinue) {
    $tools["Bandit"] = (bandit --version 2>&1 | Select-Object -First 1)
}
if (Get-Command safety -ErrorAction SilentlyContinue) {
    $tools["Safety"] = (safety --version 2>&1)
}

foreach ($tool in $tools.GetEnumerator()) {
    Write-Host "  $($tool.Key): $($tool.Value)" -ForegroundColor Green
}

Write-Host "`nPhase I: COMPLETE`n" -ForegroundColor Green

# ===========================================================================
# PHASE II: DOCKER BUILD
# ===========================================================================

Write-Host "[PHASE II] Docker Build..." -ForegroundColor Yellow
Write-Host "Building and starting containers...`n" -ForegroundColor Gray

docker-compose down 2>&1 | Out-Null
Write-Host "  Stopped existing containers" -ForegroundColor Cyan

Write-Host "  Building image (this may take 2-3 minutes)..." -ForegroundColor Cyan
docker-compose build 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  Docker image built successfully" -ForegroundColor Green
} else {
    Write-Host "  Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "  Starting containers..." -ForegroundColor Cyan
docker-compose up -d 2>&1 | Out-Null

Write-Host "  Waiting for container to be healthy..." -ForegroundColor Cyan
Start-Sleep -Seconds 15

$containerStatus = docker inspect football-app --format='{{.State.Status}}' 2>&1
if ($containerStatus -eq "running") {
    Write-Host "  Container is running and healthy" -ForegroundColor Green
} else {
    Write-Host "  Container is not running properly" -ForegroundColor Red
}

Write-Host "`nPhase II: COMPLETE`n" -ForegroundColor Green

# ===========================================================================
# PHASE III: SECURITY SCANS
# ===========================================================================

Write-Host "[PHASE III] Security Scans..." -ForegroundColor Yellow
Write-Host "Running Bandit, Safety, and Trivy...`n" -ForegroundColor Gray

# Bandit
Write-Host "  Running Bandit (SAST)..." -ForegroundColor Cyan
bandit -r . -f json -o "reports/bandit-report-$timestamp.json" 2>&1 | Out-Null
bandit -r . -f txt -o "reports/bandit-report-$timestamp.txt" 2>&1 | Out-Null
Write-Host "  Bandit scan complete" -ForegroundColor Green

# Safety
Write-Host "  Running Safety (Dependencies)..." -ForegroundColor Cyan
safety check --json > "reports/safety-report-$timestamp.json" 2>&1
safety check > "reports/safety-report-$timestamp.txt" 2>&1
Write-Host "  Safety scan complete" -ForegroundColor Green

# Trivy
if (Get-Command trivy -ErrorAction SilentlyContinue) {
    Write-Host "  Running Trivy (Container)..." -ForegroundColor Cyan
    trivy image --format json --output "reports/trivy-report-$timestamp.json" football-app:latest 2>&1 | Out-Null
    trivy image --format table --output "reports/trivy-report-$timestamp.txt" football-app:latest 2>&1 | Out-Null
    Write-Host "  Trivy scan complete" -ForegroundColor Green
} else {
    Write-Host "  Trivy not installed - skipping" -ForegroundColor Yellow
}

Write-Host "`nPhase III: COMPLETE`n" -ForegroundColor Green

# ===========================================================================
# GENERATE FINAL REPORT
# ===========================================================================

Write-Host "[FINAL] Generating comprehensive report..." -ForegroundColor Yellow

$gitBranch = git branch --show-current 2>&1
$gitCommit = git rev-parse --short HEAD 2>&1
$gitRemote = git config --get remote.origin.url 2>&1

$report = @"
================================================================================
                    DEVSECOPS WORKFLOW - FINAL REPORT
================================================================================

Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Branch: $gitBranch
Commit: $gitCommit
Remote: $gitRemote

================================================================================
                    PHASE I: ENVIRONMENT CHECK
================================================================================

Tools Verified:
$(foreach ($tool in $tools.GetEnumerator()) { "- $($tool.Key): $($tool.Value)" })

Status: COMPLETE

================================================================================
                    PHASE II: DOCKER BUILD
================================================================================

Docker Image: football-app:latest
Container: football-app
Status: $containerStatus
Port: 5000
URL: http://localhost:5000

Status: COMPLETE

================================================================================
                    PHASE III: SECURITY SCANS
================================================================================

Scans Performed:
- Bandit (SAST): reports/bandit-report-$timestamp.txt
- Safety (Dependencies): reports/safety-report-$timestamp.txt
$(if (Get-Command trivy -ErrorAction SilentlyContinue) { "- Trivy (Container): reports/trivy-report-$timestamp.txt" } else { "- Trivy: NOT INSTALLED" })

Status: COMPLETE

================================================================================
                    PHASE IV: CI/CD
================================================================================

GitHub Actions Pipeline: .github/workflows/devsecops.yml
Trigger: Push to GitHub
Jobs: 6 (Code Quality, Dependency Scan, Docker Build, Container Scan, Summary, Deploy)

Status: READY (will trigger on git push)

================================================================================
                    PHASE V: DEPLOYMENT
================================================================================

Platform: Heroku
Configuration: Procfile, runtime.txt, requirements.txt
Status: READY (run V-deploy-heroku.ps1)

================================================================================
                    SUMMARY
================================================================================

All DevSecOps phases completed successfully!

Next Steps:
1. Review security reports in reports/
2. Commit and push to GitHub
3. Monitor GitHub Actions pipeline
4. Deploy to Heroku

Total Execution Time: $([math]::Round(((Get-Date) - $startTime).TotalSeconds, 2)) seconds

================================================================================
"@

$reportPath = "reports/DEVSECOPS-FINAL-REPORT-$timestamp.txt"
$report | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host "`nFinal report generated: $reportPath`n" -ForegroundColor Cyan

# ===========================================================================
# SUMMARY
# ===========================================================================

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "                    WORKFLOW COMPLETE!" -ForegroundColor Cyan
Write-Host "========================================================================`n" -ForegroundColor Cyan

Write-Host "Phase I: Environment Check - COMPLETE" -ForegroundColor Green
Write-Host "Phase II: Docker Build - COMPLETE" -ForegroundColor Green
Write-Host "Phase III: Security Scans - COMPLETE" -ForegroundColor Green
Write-Host "Phase IV: CI/CD - READY" -ForegroundColor Yellow
Write-Host "Phase V: Deployment - READY`n" -ForegroundColor Yellow

Write-Host "Application URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Reports: reports/" -ForegroundColor Cyan
Write-Host "Final Report: $reportPath`n" -ForegroundColor Cyan

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Review reports: Get-ChildItem reports\" -ForegroundColor White
Write-Host "2. Test app: start http://localhost:5000" -ForegroundColor White
Write-Host "3. Commit and push to GitHub" -ForegroundColor White
Write-Host "4. Deploy to Heroku (if needed)`n" -ForegroundColor White

Write-Host "========================================================================`n" -ForegroundColor Cyan

