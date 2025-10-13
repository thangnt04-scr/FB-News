# Script cài đặt Trivy cho Windows
# Chạy PowerShell as Administrator

Write-Host "Installing Trivy..." -ForegroundColor Green

# Cài đặt Trivy qua Chocolatey
choco install trivy -y

Write-Host "`nVerifying installation..." -ForegroundColor Green
trivy --version

Write-Host "`nTrivy installed successfully!" -ForegroundColor Green

