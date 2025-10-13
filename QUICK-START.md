# 🚀 QUICK START - DEVSECOPS FOOTBALL APP

## 📋 TÓM TẮT

Dự án Football Information System đã được triển khai đầy đủ quy trình DevSecOps:
- ✅ Docker hóa ứng dụng
- ✅ Quét bảo mật tự động (SAST, Dependency, Container)
- ✅ CI/CD với GitHub Actions
- ✅ Sẵn sàng deploy lên Render

---

## ⚡ CHẠY NGAY (3 BƯỚC)

### **1. Chạy Security Scans (Local)**

```powershell
# Chạy tất cả security scans
.\run-devsecops-scans.ps1

# Xem báo cáo
Get-Content reports\DEVSECOPS-FINAL-REPORT-*.txt
```

**Kết quả:**
- ✅ Bandit report (SAST)
- ✅ Safety report (Dependencies)
- ✅ Trivy report (Container)

---

### **2. Build & Run Docker**

```powershell
# Build image
docker-compose build

# Start container
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Test app
curl http://localhost:5000
# Or open browser: http://localhost:5000

# Stop
docker-compose down
```

---

### **3. Deploy to Render**

```powershell
# 1. Commit changes
git add .
git commit -m "Deploy to Render"
git push origin cicd-pipeline

# 2. Tạo service trên Render
# Follow: RENDER-DEPLOYMENT-GUIDE.md

# 3. Cấu hình GitHub Secrets
# RENDER_API_KEY: rnd_rb9fxHXk9NQPpxcpCCBhiwr2RyjF
# RENDER_SERVICE_ID: (from Render Dashboard)

# 4. Verify deployment
# GitHub Actions: https://github.com/thangnt04-scr/FB-News/actions
# Render: https://dashboard.render.com/
```

---

## 📁 CẤU TRÚC DỰ ÁN

```
Football/
├── 🔒 SECURITY SCANS
│   ├── run-devsecops-scans.ps1        # Script chạy tất cả scans
│   └── reports/                        # Báo cáo security
│
├── 🐳 DOCKER
│   ├── Dockerfile                      # Production image
│   ├── docker-compose.yml              # Compose config
│   └── .dockerignore                   # Ignore rules
│
├── ☁️  CLOUD DEPLOYMENT
│   ├── render.yaml                     # Render config
│   └── build.sh                        # Build script
│
├── 🔄 CI/CD
│   └── .github/workflows/
│       └── devsecops.yml               # GitHub Actions
│
└── 📖 DOCUMENTATION
    ├── QUICK-START.md                  # This file
    ├── RENDER-DEPLOYMENT-GUIDE.md      # Deploy guide
    └── DEVSECOPS-COMPLETE-REPORT.md    # Full report
```

---

## 🔍 SECURITY SCANS

### **Bandit (SAST)**
Quét mã nguồn Python để tìm lỗ hổng bảo mật

```powershell
bandit -r . -ll --exclude ./venv
```

### **Safety (Dependencies)**
Kiểm tra dependencies có CVE

```powershell
safety check
```

### **Trivy (Container)**
Quét Docker image

```powershell
trivy image football-app:latest
```

---

## 🔄 CI/CD PIPELINE

### **Workflow:** `.github/workflows/devsecops.yml`

**Triggers:**
- Push to `main` or `cicd-pipeline`
- Pull request
- Weekly schedule (Sunday 00:00)
- Manual dispatch

**Jobs:**
1. ✅ Code Quality (Bandit, Pylint, Flake8)
2. ✅ Dependency Scan (Safety)
3. ✅ Docker Build
4. ✅ Container Scan (Trivy)
5. ✅ Security Summary
6. ✅ Deploy to Render (auto)

**View runs:**
https://github.com/thangnt04-scr/FB-News/actions

---

## ☁️  RENDER DEPLOYMENT

### **Configuration:**
- **Platform:** Render.com
- **Region:** Singapore
- **Plan:** Free Tier
- **Branch:** cicd-pipeline
- **Auto-Deploy:** Enabled

### **Files:**
- `render.yaml` - Service configuration
- `build.sh` - Build script

### **Guide:**
📄 See: `RENDER-DEPLOYMENT-GUIDE.md`

---

## 📊 REPORTS

### **Security Scan Reports:**
```
reports/
├── bandit-report-*.json
├── bandit-report-*.txt
├── safety-report-*.json
├── safety-report-*.txt
├── trivy-report-*.json
├── trivy-report-*.txt
└── DEVSECOPS-FINAL-REPORT-*.txt
```

### **View latest report:**
```powershell
# Get latest report
$latest = Get-ChildItem reports\DEVSECOPS-FINAL-REPORT-*.txt | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Get-Content $latest
```

---

## 🛠️ TROUBLESHOOTING

### **Docker build fails:**
```powershell
# Clean and rebuild
docker-compose down -v
docker system prune -f
docker-compose build --no-cache
```

### **Security scan fails:**
```powershell
# Install tools
pip install bandit safety
choco install trivy -y  # PowerShell as Admin
```

### **Port 5000 in use:**
```powershell
# Change port in docker-compose.yml
ports:
  - "5001:5000"  # Use port 5001 instead
```

---

## 📚 DOCUMENTATION

| File | Description |
|------|-------------|
| `QUICK-START.md` | This file - Quick start guide |
| `RENDER-DEPLOYMENT-GUIDE.md` | Detailed Render deployment guide |
| `DEVSECOPS-COMPLETE-REPORT.md` | Complete DevSecOps report |
| `HUONG_DAN_DEVSECOPS.md` | Vietnamese DevSecOps guide |

---

## 🔗 LINKS

- **GitHub Repo:** https://github.com/thangnt04-scr/FB-News
- **GitHub Actions:** https://github.com/thangnt04-scr/FB-News/actions
- **Render Dashboard:** https://dashboard.render.com/

---

## ✅ CHECKLIST

### **Local Development:**
- [x] ✅ Security scans completed
- [x] ✅ Docker build successful
- [x] ✅ App runs locally

### **CI/CD:**
- [x] ✅ GitHub Actions workflow configured
- [x] ✅ Automated security scans
- [x] ✅ Auto-deployment ready

### **Cloud Deployment:**
- [ ] ⏳ Create Render service
- [ ] ⏳ Configure GitHub Secrets
- [ ] ⏳ Verify deployment

---

## 🎯 NEXT STEPS

1. **Run security scans:**
   ```powershell
   .\run-devsecops-scans.ps1
   ```

2. **Test Docker locally:**
   ```powershell
   docker-compose up -d
   curl http://localhost:5000
   ```

3. **Deploy to Render:**
   - Follow `RENDER-DEPLOYMENT-GUIDE.md`

4. **Monitor CI/CD:**
   - Check GitHub Actions
   - Review security reports

---

**Ready to deploy! 🚀**

