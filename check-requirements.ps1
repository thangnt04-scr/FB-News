# Script kiểm tra tất cả requirements cho DevSecOps
# Chạy trong PowerShell

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  KIỂM TRA REQUIREMENTS DEVSECOPS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$allOk = $true

# Function để kiểm tra command
function Test-Command {
    param($CommandName, $VersionArg = "--version")
    
    try {
        $output = & $CommandName $VersionArg 2>&1
        return $true, $output
    } catch {
        return $false, $null
    }
}

# 1. Kiểm tra Python
Write-Host "1. Checking Python..." -ForegroundColor Yellow
$pythonOk, $pythonVersion = Test-Command "python"
if ($pythonOk) {
    Write-Host "   ✅ Python: $($pythonVersion[0])" -ForegroundColor Green
} else {
    Write-Host "   ❌ Python: NOT FOUND" -ForegroundColor Red
    Write-Host "      Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    $allOk = $false
}

# 2. Kiểm tra Git
Write-Host "`n2. Checking Git..." -ForegroundColor Yellow
$gitOk, $gitVersion = Test-Command "git"
if ($gitOk) {
    Write-Host "   ✅ Git: $($gitVersion[0])" -ForegroundColor Green
} else {
    Write-Host "   ❌ Git: NOT FOUND" -ForegroundColor Red
    Write-Host "      Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    $allOk = $false
}

# 3. Kiểm tra Docker
Write-Host "`n3. Checking Docker..." -ForegroundColor Yellow
$dockerOk, $dockerVersion = Test-Command "docker"
if ($dockerOk) {
    Write-Host "   ✅ Docker: $($dockerVersion[0])" -ForegroundColor Green
    
    # Kiểm tra Docker đang chạy
    try {
        docker ps | Out-Null
        Write-Host "   ✅ Docker is running" -ForegroundColor Green
    } catch {
        Write-Host "   ⚠️  Docker is installed but NOT RUNNING" -ForegroundColor Yellow
        Write-Host "      Please start Docker Desktop" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ Docker: NOT FOUND" -ForegroundColor Red
    Write-Host "      Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    $allOk = $false
}

# 4. Kiểm tra Docker Compose
Write-Host "`n4. Checking Docker Compose..." -ForegroundColor Yellow
$composeOk, $composeVersion = Test-Command "docker-compose"
if ($composeOk) {
    Write-Host "   ✅ Docker Compose: $($composeVersion[0])" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Docker Compose: NOT FOUND (usually comes with Docker Desktop)" -ForegroundColor Yellow
}

# 5. Kiểm tra Bandit
Write-Host "`n5. Checking Bandit (SAST)..." -ForegroundColor Yellow
$banditOk, $banditVersion = Test-Command "bandit"
if ($banditOk) {
    Write-Host "   ✅ Bandit: $($banditVersion[0])" -ForegroundColor Green
} else {
    Write-Host "   ❌ Bandit: NOT FOUND" -ForegroundColor Red
    Write-Host "      Installing Bandit..." -ForegroundColor Yellow
    pip install bandit
    Write-Host "   ✅ Bandit installed!" -ForegroundColor Green
}

# 6. Kiểm tra Safety
Write-Host "`n6. Checking Safety (Dependency Scanner)..." -ForegroundColor Yellow
$safetyOk, $safetyVersion = Test-Command "safety"
if ($safetyOk) {
    Write-Host "   ✅ Safety: $($safetyVersion[0])" -ForegroundColor Green
} else {
    Write-Host "   ❌ Safety: NOT FOUND" -ForegroundColor Red
    Write-Host "      Installing Safety..." -ForegroundColor Yellow
    pip install safety
    Write-Host "   ✅ Safety installed!" -ForegroundColor Green
}

# 7. Kiểm tra Trivy
Write-Host "`n7. Checking Trivy (Container Scanner)..." -ForegroundColor Yellow
$trivyOk, $trivyVersion = Test-Command "trivy"
if ($trivyOk) {
    Write-Host "   ✅ Trivy: $($trivyVersion[0])" -ForegroundColor Green
} else {
    Write-Host "   ❌ Trivy: NOT FOUND" -ForegroundColor Red
    Write-Host "      To install Trivy:" -ForegroundColor Yellow
    Write-Host "      1. Run PowerShell as Administrator" -ForegroundColor Yellow
    Write-Host "      2. Run: choco install trivy -y" -ForegroundColor Yellow
    Write-Host "      Or download from: https://github.com/aquasecurity/trivy/releases" -ForegroundColor Yellow
    $allOk = $false
}

# 8. Kiểm tra Gunicorn (Production server)
Write-Host "`n8. Checking Gunicorn (Production Server)..." -ForegroundColor Yellow
try {
    pip show gunicorn | Out-Null
    Write-Host "   ✅ Gunicorn: Installed" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Gunicorn: NOT FOUND" -ForegroundColor Red
    Write-Host "      Installing Gunicorn..." -ForegroundColor Yellow
    pip install gunicorn
    Write-Host "   ✅ Gunicorn installed!" -ForegroundColor Green
}

# 9. Kiểm tra Chocolatey (Package manager)
Write-Host "`n9. Checking Chocolatey (Package Manager)..." -ForegroundColor Yellow
$chocoOk, $chocoVersion = Test-Command "choco"
if ($chocoOk) {
    Write-Host "   ✅ Chocolatey: $($chocoVersion[0])" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Chocolatey: NOT FOUND (optional but recommended)" -ForegroundColor Yellow
    Write-Host "      Install from: https://chocolatey.org/install" -ForegroundColor Yellow
}

# 10. Kiểm tra VS Code (Optional)
Write-Host "`n10. Checking VS Code (Optional)..." -ForegroundColor Yellow
$codeOk, $codeVersion = Test-Command "code"
if ($codeOk) {
    Write-Host "   ✅ VS Code: Installed" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  VS Code: NOT FOUND (optional but recommended)" -ForegroundColor Yellow
    Write-Host "      Download from: https://code.visualstudio.com/" -ForegroundColor Yellow
}

# Tổng kết
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  SUMMARY" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

if ($allOk) {
    Write-Host "✅ ALL REQUIRED TOOLS ARE INSTALLED!" -ForegroundColor Green
    Write-Host "`nYou are ready to start with DevSecOps!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "1. Read: START_HERE.md" -ForegroundColor White
    Write-Host "2. Follow: HUONG_DAN_STEP_BY_STEP.md" -ForegroundColor White
} else {
    Write-Host "⚠️  SOME REQUIRED TOOLS ARE MISSING" -ForegroundColor Yellow
    Write-Host "`nPlease install the missing tools and run this script again." -ForegroundColor Yellow
}

Write-Host "`n========================================`n" -ForegroundColor Cyan

# Kiểm tra thêm: Project dependencies
Write-Host "Checking Project Dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "✅ requirements.txt found" -ForegroundColor Green
    
    # Kiểm tra virtual environment
    if (Test-Path "venv") {
        Write-Host "✅ Virtual environment exists" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Virtual environment not found" -ForegroundColor Yellow
        Write-Host "   Create with: python -m venv venv" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  requirements.txt not found" -ForegroundColor Yellow
}

Write-Host "`nDone!" -ForegroundColor Green

