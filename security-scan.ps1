# DevSecOps Security Scanning Script for Windows PowerShell
# Tự động quét bảo mật cho Football Information System

param(
    [switch]$SkipDocker = $false,
    [switch]$Verbose = $false
)

# Configuration
$ReportsDir = "security-reports"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ReportArchive = "security-scan-$Timestamp.zip"

# Colors
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"
$ColorInfo = "Cyan"

# Functions
function Write-Header {
    param([string]$Message)
    Write-Host "`n================================" -ForegroundColor Blue
    Write-Host $Message -ForegroundColor Blue
    Write-Host "================================`n" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor $ColorSuccess
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor $ColorWarning
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor $ColorError
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor $ColorInfo
}

# Check dependencies
function Test-Dependencies {
    Write-Header "Checking Dependencies"
    
    $missingTools = @()
    
    # Check Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        $missingTools += "python"
    }
    
    # Check Docker
    if (-not $SkipDocker) {
        if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
            $missingTools += "docker"
        }
    }
    
    # Check Bandit
    try {
        python -c "import bandit" 2>$null
    } catch {
        Write-Warning "Bandit not installed. Installing..."
        pip install bandit
    }
    
    # Check Safety
    try {
        python -c "import safety" 2>$null
    } catch {
        Write-Warning "Safety not installed. Installing..."
        pip install safety
    }
    
    # Check Trivy
    if (-not $SkipDocker) {
        if (-not (Get-Command trivy -ErrorAction SilentlyContinue)) {
            Write-Warning "Trivy not installed. Please install from: https://aquasecurity.github.io/trivy/"
            $missingTools += "trivy"
        }
    }
    
    if ($missingTools.Count -gt 0) {
        Write-Error "Missing required tools: $($missingTools -join ', ')"
        exit 1
    }
    
    Write-Success "All dependencies are installed"
}

# Setup reports directory
function Initialize-ReportsDirectory {
    Write-Header "Setting Up Reports Directory"
    
    if (Test-Path $ReportsDir) {
        Write-Info "Backing up existing reports..."
        Compress-Archive -Path $ReportsDir -DestinationPath "backup-$Timestamp.zip" -Force
        Remove-Item -Path $ReportsDir -Recurse -Force
    }
    
    New-Item -ItemType Directory -Path $ReportsDir -Force | Out-Null
    Write-Success "Reports directory created: $ReportsDir"
}

# Run Bandit SAST scan
function Invoke-BanditScan {
    Write-Header "Running Bandit (SAST)"
    
    Write-Info "Scanning Python code for security issues..."
    
    # JSON output
    bandit -r . -f json -o "$ReportsDir/bandit-report.json" 2>$null
    
    # Text output
    bandit -r . -ll > "$ReportsDir/bandit-report.txt" 2>&1
    
    # HTML output
    bandit -r . -f html -o "$ReportsDir/bandit-report.html" 2>$null
    
    # Count issues
    try {
        $banditJson = Get-Content "$ReportsDir/bandit-report.json" | ConvertFrom-Json
        $issueCount = $banditJson.results.Count
        
        if ($issueCount -gt 0) {
            Write-Warning "Found $issueCount security issues"
        } else {
            Write-Success "No security issues found"
        }
    } catch {
        Write-Warning "Could not parse Bandit results"
    }
}

# Run Safety dependency check
function Invoke-SafetyCheck {
    Write-Header "Running Safety (Dependency Check)"
    
    Write-Info "Checking for known vulnerabilities in dependencies..."
    
    # JSON output
    safety check --json --output "$ReportsDir/safety-report.json" 2>$null
    
    # Text output
    safety check --full-report > "$ReportsDir/safety-report.txt" 2>&1
    
    # Count vulnerabilities
    try {
        $safetyJson = Get-Content "$ReportsDir/safety-report.json" | ConvertFrom-Json
        $vulnCount = $safetyJson.Count
        
        if ($vulnCount -gt 0) {
            Write-Warning "Found $vulnCount vulnerabilities in dependencies"
        } else {
            Write-Success "No vulnerabilities found in dependencies"
        }
    } catch {
        Write-Success "No vulnerabilities found in dependencies"
    }
}

# Build Docker image
function Build-DockerImage {
    Write-Header "Building Docker Image"
    
    Write-Info "Building football-app:latest..."
    
    try {
        docker build -t football-app:latest . > "$ReportsDir/docker-build.log" 2>&1
        Write-Success "Docker image built successfully"
    } catch {
        Write-Error "Failed to build Docker image"
        Get-Content "$ReportsDir/docker-build.log"
        exit 1
    }
}

# Run Trivy container scan
function Invoke-TrivyScan {
    Write-Header "Running Trivy (Container Scan)"
    
    Write-Info "Scanning Docker image for vulnerabilities..."
    
    # JSON output
    trivy image -f json -o "$ReportsDir/trivy-report.json" football-app:latest 2>$null
    
    # Text output
    trivy image football-app:latest > "$ReportsDir/trivy-report.txt" 2>&1
    
    # Critical and High only
    trivy image --severity HIGH,CRITICAL football-app:latest > "$ReportsDir/trivy-critical.txt" 2>&1
    
    # Count vulnerabilities
    try {
        $trivyJson = Get-Content "$ReportsDir/trivy-report.json" | ConvertFrom-Json
        $vulns = $trivyJson.Results[0].Vulnerabilities
        $criticalCount = ($vulns | Where-Object { $_.Severity -eq "CRITICAL" }).Count
        $highCount = ($vulns | Where-Object { $_.Severity -eq "HIGH" }).Count
        
        if ($criticalCount -gt 0 -or $highCount -gt 0) {
            Write-Warning "Found $criticalCount CRITICAL and $highCount HIGH vulnerabilities"
        } else {
            Write-Success "No critical or high vulnerabilities found"
        }
    } catch {
        Write-Warning "Could not parse Trivy results"
    }
}

# Generate summary report
function New-SummaryReport {
    Write-Header "Generating Summary Report"
    
    $summaryScript = @"
import json
import os
from datetime import datetime

def load_json(filepath):
    try:
        with open(filepath, encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

# Load reports
bandit_data = load_json('$ReportsDir/bandit-report.json')
safety_data = load_json('$ReportsDir/safety-report.json')
trivy_data = load_json('$ReportsDir/trivy-report.json')

# Generate markdown
print("# Security Scan Summary Report")
print(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n**Project:** Football Information System")
print("\n---\n")

# Bandit results
print("## 🔍 Bandit (SAST) Results\n")
if bandit_data:
    results = bandit_data.get('results', [])
    high = sum(1 for r in results if r.get('issue_severity') == 'HIGH')
    medium = sum(1 for r in results if r.get('issue_severity') == 'MEDIUM')
    low = sum(1 for r in results if r.get('issue_severity') == 'LOW')
    
    print(f"- **Total Issues:** {len(results)}")
    print(f"- **High Severity:** {high}")
    print(f"- **Medium Severity:** {medium}")
    print(f"- **Low Severity:** {low}")
else:
    print("- No data available")

# Safety results
print("\n## 🔒 Safety (Dependencies) Results\n")
if safety_data:
    print(f"- **Vulnerabilities Found:** {len(safety_data)}")
else:
    print("- No vulnerabilities found")

# Trivy results
print("\n## 🐳 Trivy (Container) Results\n")
if trivy_data:
    results = trivy_data.get('Results', [])
    if results and results[0].get('Vulnerabilities'):
        vulns = results[0].get('Vulnerabilities', [])
        critical = sum(1 for v in vulns if v.get('Severity') == 'CRITICAL')
        high = sum(1 for v in vulns if v.get('Severity') == 'HIGH')
        medium = sum(1 for v in vulns if v.get('Severity') == 'MEDIUM')
        low = sum(1 for v in vulns if v.get('Severity') == 'LOW')
        
        print(f"- **Total Vulnerabilities:** {len(vulns)}")
        print(f"- **Critical:** {critical}")
        print(f"- **High:** {high}")
        print(f"- **Medium:** {medium}")
        print(f"- **Low:** {low}")
    else:
        print("- No vulnerabilities found")
else:
    print("- No data available")

print("\n---\n")
print("## 📊 Recommendations\n")
print("1. Review and fix all HIGH and CRITICAL severity issues")
print("2. Update vulnerable dependencies to latest secure versions")
print("3. Implement security best practices from OWASP Top 10")
print("4. Schedule regular security scans (weekly/monthly)")
print("5. Enable automated security scanning in CI/CD pipeline")
"@
    
    python -c $summaryScript > "$ReportsDir/summary.md"
    Write-Success "Summary report generated"
}

# Archive reports
function Compress-Reports {
    Write-Header "Archiving Reports"
    
    Compress-Archive -Path $ReportsDir -DestinationPath $ReportArchive -Force
    Write-Success "Reports archived: $ReportArchive"
}

# Display summary
function Show-Summary {
    Write-Header "Scan Summary"
    
    if (Test-Path "$ReportsDir/summary.md") {
        Get-Content "$ReportsDir/summary.md"
    }
    
    Write-Host ""
    Write-Info "Detailed reports available in: $ReportsDir"
    Write-Info "Archive created: $ReportArchive"
}

# Main execution
function Main {
    Write-Header "DevSecOps Security Scan"
    Write-Host "Starting security scan at $(Get-Date)" -ForegroundColor Cyan
    Write-Host ""
    
    Test-Dependencies
    Initialize-ReportsDirectory
    Invoke-BanditScan
    Invoke-SafetyCheck
    
    if (-not $SkipDocker) {
        Build-DockerImage
        Invoke-TrivyScan
    } else {
        Write-Warning "Skipping Docker-related scans"
    }
    
    New-SummaryReport
    Compress-Reports
    Show-Summary
    
    Write-Host ""
    Write-Success "Security scan completed successfully!"
    Write-Info "Review the reports and address any security issues found."
}

# Run main function
try {
    Main
} catch {
    Write-Error "An error occurred: $_"
    exit 1
}

