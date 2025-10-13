# 🚀 HƯỚNG DẪN DEVSECOPS - Football Information System

**Thời gian:** 2-3 giờ | **Mức độ:** Beginner-friendly | **Mục tiêu:** Triển khai đầy đủ DevSecOps

---

## 📋 MỤC LỤC

1. [Giới Thiệu](#1-giới-thiệu)
2. [Chuẩn Bị Môi Trường](#2-chuẩn-bị-môi-trường)
3. [Docker Hóa Ứng Dụng](#3-docker-hóa-ứng-dụng)
4. [Quét Bảo Mật](#4-quét-bảo-mật)
5. [CI/CD Pipeline](#5-cicd-pipeline)
6. [Triển Khai Cloud](#6-triển-khai-cloud)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. GIỚI THIỆU

### 🎯 Mục Tiêu
- ✅ Docker hóa ứng dụng Flask
- ✅ Quét bảo mật tự động (SAST, Dependency, Container)
- ✅ CI/CD với GitHub Actions
- ✅ Deploy lên Cloud (AWS/GCP/Azure/Heroku)

### 🛠️ Công Nghệ
- **Backend:** Python 3.11+, Flask 3.0.0, Gunicorn 21.2.0
- **Container:** Docker, Docker Compose
- **Security:** Bandit (SAST), Safety (Dependency), Trivy (Container)
- **CI/CD:** GitHub Actions
- **Cloud:** AWS, GCP, Azure, Heroku

### 📊 Kiến Trúc

```
Developer → Git Push → GitHub Actions → Security Scans → Deploy → Cloud
```

---

## 2. CHUẨN BỊ MÔI TRƯỜNG

### ✅ Checklist Công Cụ

| Công cụ | Version | Cài đặt |
|---------|---------|---------|
| Python | 3.11+ | https://python.org |
| Git | Latest | https://git-scm.com |
| Docker Desktop | Latest | https://docker.com |
| VS Code | Latest | https://code.visualstudio.com |

### 📦 Cài Đặt

#### Windows
```powershell
# 1. Kiểm tra Python
python --version

# 2. Kiểm tra Git
git --version

# 3. Kiểm tra Docker
docker --version

# 4. Clone dự án
git clone https://github.com/thangnt04-scr/FB-News.git
cd FB-News

# 5. Tạo virtual environment
python -m venv venv
venv\Scripts\activate

# 6. Cài dependencies
pip install -r requirements.txt

# 7. Cài security tools
pip install bandit safety

# 8. Cài Trivy (PowerShell as Admin)
choco install trivy -y
```

#### Linux/Mac
```bash
# 1-4: Tương tự Windows

# 5. Activate venv
source venv/bin/activate

# 6-7: Tương tự Windows

# 8. Cài Trivy
# Mac:
brew install trivy
# Linux:
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

### ✅ Kiểm Tra
```powershell
# Chạy script kiểm tra
.\check-requirements.ps1

# Kết quả mong đợi:
# ✅ Python 3.11+
# ✅ Git
# ✅ Docker
# ✅ Bandit
# ✅ Safety
# ✅ Trivy
```

---

## 3. DOCKER HÓA ỨNG DỤNG

### 📁 Files Cần Thiết

#### 1. requirements.txt
```
Flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
Flask-Login==0.6.3
Werkzeug==3.0.1
gunicorn==21.2.0
```

#### 2. Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
```

#### 3. docker-compose.yml
```yaml
services:
  web:
    build: .
    image: football-app:latest
    container_name: football-app
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY:-your-secret-key}
    volumes:
      - ./footballinfor.db:/app/footballinfor.db
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M

networks:
  default:
    driver: bridge
```

#### 4. .dockerignore
```
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.git/
.gitignore
*.md
.env
.vscode/
*.log
```

### 🚀 Build và Run

```powershell
# 1. Build image
docker-compose build

# 2. Start container
docker-compose up -d

# 3. Check status
docker-compose ps

# Expected output:
# NAME            STATUS          PORTS
# football-app    Up (healthy)    0.0.0.0:5000->5000/tcp

# 4. View logs
docker-compose logs -f

# Expected output:
# [INFO] Starting gunicorn 21.2.0
# [INFO] Listening at: http://0.0.0.0:5000
# [INFO] Booting worker with pid: 8-11

# 5. Test
curl http://localhost:5000
# Or open browser: http://localhost:5000

# 6. Stop
docker-compose down
```

### 🐛 Troubleshooting Docker

#### Container keeps restarting
```powershell
# Check logs
docker logs football-app

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### Cannot access localhost:5000
```powershell
# 1. Check container status
docker ps

# 2. Check Docker Desktop is running

# 3. Try different port
# Edit docker-compose.yml: "5001:5000"
docker-compose up -d
```

---

## 4. QUÉT BẢO MẬT

### 🔒 Security Tools

| Tool | Purpose | Scans |
|------|---------|-------|
| **Bandit** | SAST | Python code vulnerabilities |
| **Safety** | Dependency | Known vulnerabilities in packages |
| **Trivy** | Container | Docker image vulnerabilities |

### 📝 security-scan.ps1

```powershell
# Security Scanning Script
Write-Host "=== DEVSECOPS SECURITY SCAN ===" -ForegroundColor Cyan

# 1. Bandit - SAST
Write-Host "`n[1/3] Running Bandit (SAST)..." -ForegroundColor Yellow
bandit -r . -f json -o reports/bandit-report.json
bandit -r . -f txt -o reports/bandit-report.txt
Write-Host "✅ Bandit scan complete" -ForegroundColor Green

# 2. Safety - Dependency Scan
Write-Host "`n[2/3] Running Safety (Dependency)..." -ForegroundColor Yellow
safety check --json > reports/safety-report.json
safety check > reports/safety-report.txt
Write-Host "✅ Safety scan complete" -ForegroundColor Green

# 3. Trivy - Container Scan
Write-Host "`n[3/3] Running Trivy (Container)..." -ForegroundColor Yellow
trivy image --format json --output reports/trivy-report.json football-app:latest
trivy image --format table --output reports/trivy-report.txt football-app:latest
Write-Host "✅ Trivy scan complete" -ForegroundColor Green

Write-Host "`n=== SCAN COMPLETE ===" -ForegroundColor Cyan
Write-Host "Reports saved in: reports/" -ForegroundColor Green
```

### 🚀 Chạy Security Scans

```powershell
# 1. Tạo thư mục reports
New-Item -ItemType Directory -Path reports -Force

# 2. Chạy scans
.\security-scan.ps1

# 3. Xem kết quả
Get-ChildItem reports\

# Expected files:
# bandit-report.json
# bandit-report.txt
# safety-report.json
# safety-report.txt
# trivy-report.json
# trivy-report.txt
```

### 📊 Phân Tích Kết Quả

```powershell
# Xem Bandit report
type reports\bandit-report.txt

# Xem Safety report
type reports\safety-report.txt

# Xem Trivy report
type reports\trivy-report.txt
```

---

## 5. CI/CD PIPELINE

### 📝 .github/workflows/devsecops.yml

```yaml
name: DevSecOps Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install bandit safety
      
      - name: Run Bandit
        run: bandit -r . -f json -o bandit-report.json
        continue-on-error: true
      
      - name: Run Safety
        run: safety check --json > safety-report.json
        continue-on-error: true
      
      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            bandit-report.json
            safety-report.json
  
  docker-build:
    runs-on: ubuntu-latest
    needs: security-scan
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t football-app:latest .
      
      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: football-app:latest
          format: 'json'
          output: 'trivy-report.json'
      
      - name: Upload Trivy report
        uses: actions/upload-artifact@v3
        with:
          name: trivy-report
          path: trivy-report.json
```

### 🚀 Setup GitHub Actions

```powershell
# 1. Tạo thư mục
New-Item -ItemType Directory -Path .github\workflows -Force

# 2. Tạo file workflow (đã có sẵn)

# 3. Commit và push
git add .
git commit -m "Add DevSecOps pipeline"
git push origin main

# 4. Xem pipeline chạy
# Truy cập: https://github.com/your-username/FB-News/actions
```

---

## 6. TRIỂN KHAI CLOUD

### ☁️ Heroku (Nhanh nhất - 5 phút)

```powershell
# 1. Cài Heroku CLI
# Download: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Tạo app
heroku create football-app-devsecops

# 4. Deploy
git push heroku main

# 5. Open app
heroku open

# 6. View logs
heroku logs --tail
```

### ☁️ Google Cloud Run

```powershell
# 1. Cài gcloud CLI
# Download: https://cloud.google.com/sdk/docs/install

# 2. Login
gcloud auth login

# 3. Set project
gcloud config set project YOUR_PROJECT_ID

# 4. Build và deploy
gcloud run deploy football-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# 5. Get URL
gcloud run services describe football-app --region us-central1
```

### ☁️ AWS Elastic Beanstalk

```powershell
# 1. Cài EB CLI
pip install awsebcli

# 2. Initialize
eb init -p docker football-app

# 3. Create environment
eb create football-env

# 4. Deploy
eb deploy

# 5. Open app
eb open

# 6. View logs
eb logs
```

---

## 7. TROUBLESHOOTING

### 🐛 Docker Issues

**Container keeps restarting:**
```powershell
docker logs football-app
docker-compose build --no-cache
docker-compose up -d
```

**Port already in use:**
```powershell
# Find process
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

**Permission denied:**
```powershell
# Rebuild with correct permissions
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 🔒 Security Scan Issues

**Trivy not found:**
```powershell
# Install Trivy
choco install trivy -y

# Verify
trivy --version
```

**Bandit/Safety errors:**
```powershell
# Reinstall
pip uninstall bandit safety
pip install bandit safety

# Verify
bandit --version
safety --version
```

### ☁️ Deployment Issues

**Heroku build fails:**
```powershell
# Check Procfile exists
type Procfile

# Check runtime.txt
type runtime.txt

# View build logs
heroku logs --tail
```

**Cloud Run fails:**
```powershell
# Check Dockerfile
docker build -t test .
docker run -p 5000:5000 test

# View Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision"
```

---

## 8. LỆNH THAM KHẢO NHANH

### Docker
```powershell
docker-compose up -d          # Start
docker-compose down           # Stop
docker-compose ps             # Status
docker-compose logs -f        # Logs
docker-compose build          # Build
docker-compose restart        # Restart
```

### Security
```powershell
bandit -r .                   # SAST scan
safety check                  # Dependency scan
trivy image football-app      # Container scan
.\security-scan.ps1           # Run all scans
```

### Git
```powershell
git add .                     # Stage changes
git commit -m "message"       # Commit
git push origin main          # Push
git status                    # Check status
```

---

## ✅ CHECKLIST HOÀN THÀNH

- [ ] Python 3.11+ installed
- [ ] Docker Desktop installed
- [ ] Git installed
- [ ] Security tools installed (Bandit, Safety, Trivy)
- [ ] Project cloned
- [ ] Dependencies installed
- [ ] Docker image built
- [ ] Container running successfully
- [ ] Security scans completed
- [ ] GitHub Actions configured
- [ ] Deployed to cloud

---

<div align="center">

## 🎉 HOÀN THÀNH!

**Application:** http://localhost:5000  
**Documentation:** HUONG_DAN_DEVSECOPS.md  
**Support:** GitHub Issues  

**Made with ❤️ for secure software development**

</div>

