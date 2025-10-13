#!/bin/bash

###############################################################################
# DevSecOps Security Scanning Script
# Tự động quét bảo mật cho Football Information System
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPORTS_DIR="security-reports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_ARCHIVE="security-scan-${TIMESTAMP}.tar.gz"

# Functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if required tools are installed
check_dependencies() {
    print_header "Checking Dependencies"
    
    local missing_tools=()
    
    if ! command -v python3 &> /dev/null; then
        missing_tools+=("python3")
    fi
    
    if ! command -v docker &> /dev/null; then
        missing_tools+=("docker")
    fi
    
    if ! python3 -c "import bandit" &> /dev/null; then
        print_warning "Bandit not installed. Installing..."
        pip install bandit
    fi
    
    if ! python3 -c "import safety" &> /dev/null; then
        print_warning "Safety not installed. Installing..."
        pip install safety
    fi
    
    if ! command -v trivy &> /dev/null; then
        print_warning "Trivy not installed. Please install from: https://aquasecurity.github.io/trivy/"
        missing_tools+=("trivy")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi
    
    print_success "All dependencies are installed"
}

# Create reports directory
setup_reports_dir() {
    print_header "Setting Up Reports Directory"
    
    if [ -d "$REPORTS_DIR" ]; then
        print_info "Backing up existing reports..."
        tar -czf "backup-${TIMESTAMP}.tar.gz" "$REPORTS_DIR"
        rm -rf "$REPORTS_DIR"
    fi
    
    mkdir -p "$REPORTS_DIR"
    print_success "Reports directory created: $REPORTS_DIR"
}

# Run Bandit SAST scan
run_bandit() {
    print_header "Running Bandit (SAST)"
    
    print_info "Scanning Python code for security issues..."
    
    # JSON output
    bandit -r . -f json -o "${REPORTS_DIR}/bandit-report.json" 2>/dev/null || true
    
    # Text output
    bandit -r . -ll > "${REPORTS_DIR}/bandit-report.txt" 2>&1 || true
    
    # HTML output (if bandit supports it)
    bandit -r . -f html -o "${REPORTS_DIR}/bandit-report.html" 2>/dev/null || true
    
    # Count issues
    local issue_count=$(grep -c "issue_severity" "${REPORTS_DIR}/bandit-report.json" 2>/dev/null || echo "0")
    
    if [ "$issue_count" -gt 0 ]; then
        print_warning "Found $issue_count security issues"
    else
        print_success "No security issues found"
    fi
}

# Run Safety dependency check
run_safety() {
    print_header "Running Safety (Dependency Check)"
    
    print_info "Checking for known vulnerabilities in dependencies..."
    
    # JSON output
    safety check --json --output "${REPORTS_DIR}/safety-report.json" 2>/dev/null || true
    
    # Text output
    safety check --full-report > "${REPORTS_DIR}/safety-report.txt" 2>&1 || true
    
    # Count vulnerabilities
    local vuln_count=$(python3 -c "
import json
try:
    with open('${REPORTS_DIR}/safety-report.json') as f:
        data = json.load(f)
        print(len(data))
except:
    print(0)
" 2>/dev/null || echo "0")
    
    if [ "$vuln_count" -gt 0 ]; then
        print_warning "Found $vuln_count vulnerabilities in dependencies"
    else
        print_success "No vulnerabilities found in dependencies"
    fi
}

# Build Docker image
build_docker_image() {
    print_header "Building Docker Image"
    
    print_info "Building football-app:latest..."
    
    if docker build -t football-app:latest . > "${REPORTS_DIR}/docker-build.log" 2>&1; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        cat "${REPORTS_DIR}/docker-build.log"
        exit 1
    fi
}

# Run Trivy container scan
run_trivy() {
    print_header "Running Trivy (Container Scan)"
    
    print_info "Scanning Docker image for vulnerabilities..."
    
    # JSON output
    trivy image -f json -o "${REPORTS_DIR}/trivy-report.json" football-app:latest 2>/dev/null || true
    
    # Text output
    trivy image football-app:latest > "${REPORTS_DIR}/trivy-report.txt" 2>&1 || true
    
    # Table output with only HIGH and CRITICAL
    trivy image --severity HIGH,CRITICAL football-app:latest > "${REPORTS_DIR}/trivy-critical.txt" 2>&1 || true
    
    # Count vulnerabilities
    local critical_count=$(grep -c '"Severity": "CRITICAL"' "${REPORTS_DIR}/trivy-report.json" 2>/dev/null || echo "0")
    local high_count=$(grep -c '"Severity": "HIGH"' "${REPORTS_DIR}/trivy-report.json" 2>/dev/null || echo "0")
    
    if [ "$critical_count" -gt 0 ] || [ "$high_count" -gt 0 ]; then
        print_warning "Found $critical_count CRITICAL and $high_count HIGH vulnerabilities"
    else
        print_success "No critical or high vulnerabilities found"
    fi
}

# Generate summary report
generate_summary() {
    print_header "Generating Summary Report"
    
    python3 << 'EOF' > "${REPORTS_DIR}/summary.md"
import json
import os
from datetime import datetime

def load_json(filepath):
    try:
        with open(filepath) as f:
            return json.load(f)
    except:
        return None

# Load reports
bandit_data = load_json('security-reports/bandit-report.json')
safety_data = load_json('security-reports/safety-report.json')
trivy_data = load_json('security-reports/trivy-report.json')

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
    if safety_data:
        print("\n### Details:")
        for vuln in safety_data[:5]:  # Show first 5
            print(f"- {vuln.get('package', 'Unknown')}: {vuln.get('vulnerability', 'N/A')}")
else:
    print("- No vulnerabilities found")

# Trivy results
print("\n## 🐳 Trivy (Container) Results\n")
if trivy_data:
    results = trivy_data.get('Results', [])
    if results:
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

print("\n---\n")
print("*For detailed reports, check individual files in the security-reports directory.*")
EOF
    
    print_success "Summary report generated"
}

# Archive reports
archive_reports() {
    print_header "Archiving Reports"
    
    tar -czf "$REPORT_ARCHIVE" "$REPORTS_DIR"
    print_success "Reports archived: $REPORT_ARCHIVE"
}

# Display summary
display_summary() {
    print_header "Scan Summary"
    
    if [ -f "${REPORTS_DIR}/summary.md" ]; then
        cat "${REPORTS_DIR}/summary.md"
    fi
    
    echo ""
    print_info "Detailed reports available in: $REPORTS_DIR"
    print_info "Archive created: $REPORT_ARCHIVE"
}

# Main execution
main() {
    print_header "DevSecOps Security Scan"
    echo "Starting security scan at $(date)"
    echo ""
    
    check_dependencies
    setup_reports_dir
    run_bandit
    run_safety
    build_docker_image
    run_trivy
    generate_summary
    archive_reports
    display_summary
    
    echo ""
    print_success "Security scan completed successfully!"
    print_info "Review the reports and address any security issues found."
}

# Run main function
main "$@"

