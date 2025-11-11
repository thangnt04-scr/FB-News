# ===========================================================================
#                    DEVSECOPS SECURITY SCAN SCRIPT
# ===========================================================================

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$reportDir = "reports"

# Create reports directory
if (-not (Test-Path $reportDir)) {
    New-Item -ItemType Directory -Path $reportDir | Out-Null
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     DEVSECOPS SECURITY SCAN - FOOTBALL APP" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# ===========================================================================
# 1. BANDIT - SAST
# ===========================================================================
Write-Host "[1/4] Running Bandit (SAST)..." -ForegroundColor Yellow

try {
    bandit -r . -f json -o "$reportDir/bandit-report-$timestamp.json" --exclude ./venv,./env,./.venv 2>&1 | Out-Null
    bandit -r . -f txt -o "$reportDir/bandit-report-$timestamp.txt" --exclude ./venv,./env,./.venv 2>&1 | Out-Null
    Write-Host "      [OK] Bandit scan completed" -ForegroundColor Green
}
catch {
    Write-Host "      [ERROR] Bandit scan failed" -ForegroundColor Red
}

Write-Host ""

# ===========================================================================
# 2. SAFETY - Dependency Scan
# ===========================================================================
Write-Host "[2/4] Running Safety (Dependency Scan)..." -ForegroundColor Yellow

try {
    safety check --json --output "$reportDir/safety-report-$timestamp.json" 2>&1 | Out-Null
    safety check --output text > "$reportDir/safety-report-$timestamp.txt" 2>&1
    Write-Host "      [OK] Safety scan completed" -ForegroundColor Green
}
catch {
    Write-Host "      [ERROR] Safety scan failed" -ForegroundColor Red
}

Write-Host ""

# ===========================================================================
# 3. TRIVY - Container Scan
# ===========================================================================
Write-Host "[3/4] Running Trivy (Container Scan)..." -ForegroundColor Yellow

try {
    $imageExists = docker images -q football-app:latest
    
    if (-not $imageExists) {
        Write-Host "      Building Docker image..." -ForegroundColor Yellow
        docker-compose build 2>&1 | Out-Null
    }
    
    trivy image --format json --output "$reportDir/trivy-report-$timestamp.json" football-app:latest 2>&1 | Out-Null
    trivy image --format table --output "$reportDir/trivy-report-$timestamp.txt" football-app:latest 2>&1 | Out-Null
    Write-Host "      [OK] Trivy scan completed" -ForegroundColor Green
}
catch {
    Write-Host "      [ERROR] Trivy scan failed" -ForegroundColor Red
}

Write-Host ""

# ===========================================================================
# 4. GENERATE SUMMARY
# ===========================================================================
Write-Host "[4/4] Generating Summary Report..." -ForegroundColor Yellow

$summaryFile = "$reportDir/DEVSECOPS-FINAL-REPORT-$timestamp.txt"
$branch = git rev-parse --abbrev-ref HEAD 2>$null
$commit = git rev-parse --short HEAD 2>$null

$summary = @"
================================================================
            DEVSECOPS SECURITY SCAN REPORT
================================================================

SCAN DATE: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
PROJECT: Football Information System
BRANCH: $branch
COMMIT: $commit

================================================================
SCAN SUMMARY
================================================================

1. BANDIT (SAST - Static Application Security Testing)
   - Tool: Bandit v1.8.6
   - Target: Python source code
   - Report: bandit-report-$timestamp.json
   - Status: $(if (Test-Path "$reportDir/bandit-report-$timestamp.json") { "Completed" } else { "Failed" })

2. SAFETY (Dependency Vulnerability Scan)
   - Tool: Safety v3.6.2
   - Target: Python dependencies
   - Report: safety-report-$timestamp.json
   - Status: $(if (Test-Path "$reportDir/safety-report-$timestamp.json") { "Completed" } else { "Failed" })

3. TRIVY (Container Security Scan)
   - Tool: Trivy v0.67.2
   - Target: Docker image (football-app:latest)
   - Report: trivy-report-$timestamp.json
   - Status: $(if (Test-Path "$reportDir/trivy-report-$timestamp.json") { "Completed" } else { "Failed" })

================================================================
DETAILED REPORTS
================================================================

All reports are available in the 'reports/' directory:
- bandit-report-$timestamp.json
- bandit-report-$timestamp.txt
- safety-report-$timestamp.json
- safety-report-$timestamp.txt
- trivy-report-$timestamp.json
- trivy-report-$timestamp.txt

================================================================
NEXT STEPS
================================================================

1. Review all reports in the 'reports/' directory
2. Fix any HIGH or CRITICAL vulnerabilities
3. Update dependencies if needed
4. Re-run scans to verify fixes
5. Commit and push to trigger CI/CD pipeline

================================================================
"@

$summary | Out-File -FilePath $summaryFile -Encoding UTF8

Write-Host "      [OK] Summary report generated" -ForegroundColor Green
Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "     SECURITY SCAN COMPLETED" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Reports saved to: $reportDir/" -ForegroundColor Cyan
Write-Host "Summary report: $summaryFile" -ForegroundColor Cyan
Write-Host ""

