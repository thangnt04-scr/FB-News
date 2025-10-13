# ☁️ RENDER DEPLOYMENT GUIDE - FOOTBALL APP

## 📋 MỤC LỤC

1. [Render là gì?](#render-là-gì)
2. [Tại sao chọn Render thay vì Heroku?](#tại-sao-chọn-render)
3. [Chuẩn bị](#chuẩn-bị)
4. [Deploy lên Render](#deploy-lên-render)
5. [Tích hợp CI/CD với GitHub Actions](#tích-hợp-cicd)
6. [Quản lý và monitoring](#quản-lý)
7. [Troubleshooting](#troubleshooting)

---

## 🌐 RENDER LÀ GÌ?

**Render** là một Platform as a Service (PaaS) hiện đại, thay thế tốt cho Heroku:

### **Ưu điểm:**
- ✅ **Free tier tốt hơn Heroku** (750 giờ/tháng)
- ✅ **Không sleep** như Heroku free tier
- ✅ **Auto-deploy** từ GitHub
- ✅ **Free SSL** certificates
- ✅ **Free PostgreSQL** database
- ✅ **Faster deployment** (Docker support)
- ✅ **Better pricing** ($7/month vs Heroku $25/month)
- ✅ **Modern infrastructure**

### **So sánh với Heroku:**

| Feature | **Render Free** | **Heroku Free** |
|---------|----------------|-----------------|
| **Giá** | $0 | $0 (discontinued) |
| **Sleep** | ❌ Không | ✅ Sau 30 phút |
| **Build time** | Nhanh hơn | Chậm hơn |
| **SSL** | ✅ Free | ✅ Free |
| **Database** | ✅ PostgreSQL free | ❌ Addon required |
| **Auto-deploy** | ✅ Có | ✅ Có |
| **Docker** | ✅ Native support | ⚠️ Limited |

**Website:** https://render.com

---

## 🎯 TẠI SAO CHỌN RENDER?

### **1. Heroku đã ngừng Free Tier (2022)**
- Heroku free dynos không còn từ 28/11/2022
- Phải trả tối thiểu $7/month

### **2. Render có Free Tier tốt hơn**
- 750 giờ/tháng miễn phí
- Không sleep (luôn online)
- PostgreSQL database miễn phí

### **3. Tích hợp tốt với GitHub**
- Auto-deploy khi push code
- Preview environments cho PR
- Rollback dễ dàng

### **4. Performance tốt hơn**
- Build nhanh hơn
- Cold start nhanh hơn
- Infrastructure hiện đại hơn

---

## 🔧 CHUẨN BỊ

### **Files Cần Thiết (✅ Đã có sẵn)**

```
D:\Football\
├── render.yaml              # Render configuration
├── build.sh                 # Build script
├── requirements.txt         # Python dependencies
├── app.py                   # Flask application
└── .env                     # Environment variables (local only)
```

### **Kiểm tra Files**

#### 1. **render.yaml**
```yaml
services:
  - type: web
    name: football-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
```

#### 2. **build.sh**
```bash
#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. **requirements.txt**
```
Flask==3.0.0
gunicorn==21.2.0
requests==2.31.0
python-dotenv==1.0.0
Flask-Login==0.6.3
Werkzeug==3.0.1
```

---

## 🚀 DEPLOY LÊN RENDER

### **Bước 1: Tạo Tài Khoản Render**

1. Truy cập: https://render.com
2. Click **"Get Started"**
3. Sign up với GitHub account
4. Authorize Render to access GitHub

### **Bước 2: Tạo Web Service**

1. **Dashboard** → Click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Select: `thangnt04-scr/FB-News`
   - Click **"Connect"**

3. **Configure Service:**
   ```
   Name: football-app
   Region: Singapore (hoặc gần nhất)
   Branch: main (hoặc devsecops-complete)
   Runtime: Python 3
   Build Command: ./build.sh
   Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
   ```

4. **Environment Variables:**
   ```
   SECRET_KEY = [Auto-generate]
   FLASK_ENV = production
   PYTHON_VERSION = 3.11.0
   ```

5. **Plan:**
   - Select: **Free** ($0/month)
   - Click **"Create Web Service"**

### **Bước 3: Đợi Deployment**

```
Building...
├─ Installing Python 3.11
├─ Installing dependencies
├─ Running build.sh
└─ Starting gunicorn

Deploy successful! 🎉
Live at: https://football-app.onrender.com
```

**Thời gian:** ~3-5 phút

### **Bước 4: Verify Deployment**

```bash
# Test URL
curl https://football-app.onrender.com

# Hoặc mở browser
start https://football-app.onrender.com
```

---

## 🔄 TÍCH HỢP CI/CD VỚI GITHUB ACTIONS

### **Auto-Deploy từ GitHub**

Render tự động deploy khi:
- ✅ Push to main branch
- ✅ Merge pull request
- ✅ Manual trigger

### **Trigger Deploy từ GitHub Actions**

#### **Bước 1: Lấy Render API Key**

1. Render Dashboard → **Account Settings**
2. **API Keys** → **Create API Key**
3. Copy API key

#### **Bước 2: Lấy Service ID**

1. Render Dashboard → **football-app**
2. URL sẽ có dạng: `https://dashboard.render.com/web/srv-XXXXX`
3. Copy `srv-XXXXX` (Service ID)

#### **Bước 3: Add GitHub Secrets**

1. GitHub → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret:**
   ```
   Name: RENDER_API_KEY
   Value: [Your Render API Key]
   
   Name: RENDER_SERVICE_ID
   Value: srv-XXXXX
   ```

#### **Bước 4: Workflow đã được cấu hình**

File `.github/workflows/devsecops.yml` đã có deploy job:

```yaml
deploy:
  name: Deploy to Render
  runs-on: ubuntu-latest
  needs: [security-summary]
  if: github.ref == 'refs/heads/main'
  
  steps:
    - name: Deploy to Render
      env:
        RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
      run: |
        curl -X POST "https://api.render.com/v1/services/${{ secrets.RENDER_SERVICE_ID }}/deploys" \
          -H "Authorization: Bearer $RENDER_API_KEY"
```

### **Workflow Hoàn Chỉnh:**

```
1. Push code to GitHub
   ↓
2. GitHub Actions CI/CD
   ├─ Code quality checks
   ├─ Security scans
   ├─ Docker build
   └─ All tests pass ✅
   ↓
3. Auto-deploy to Render
   ↓
4. Render builds and deploys
   ↓
5. App live at: https://football-app.onrender.com
```

---

## 🔍 QUẢN LÝ VÀ MONITORING

### **View Logs**

1. Render Dashboard → **football-app**
2. **Logs** tab
3. Real-time logs

### **Environment Variables**

1. **Environment** tab
2. Add/Edit variables
3. Click **Save Changes** (auto-redeploy)

### **Manual Deploy**

1. **Manual Deploy** button
2. Select branch
3. **Deploy**

### **Rollback**

1. **Events** tab
2. Find previous successful deploy
3. **Rollback to this version**

### **Custom Domain**

1. **Settings** tab
2. **Custom Domain**
3. Add your domain
4. Update DNS records

---

## ❌ TROUBLESHOOTING

### **Problem 1: Build Failed**

**Error:**
```
Build failed: pip install error
```

**Solution:**
```bash
# Check build.sh permissions
chmod +x build.sh

# Verify requirements.txt
cat requirements.txt

# Test locally
pip install -r requirements.txt
```

### **Problem 2: Application Error**

**Error:**
```
Application failed to respond
```

**Solution:**
```bash
# Check start command
gunicorn --bind 0.0.0.0:$PORT app:app

# Verify PORT environment variable
echo $PORT

# Check logs in Render dashboard
```

### **Problem 3: Database Error**

**Error:**
```
sqlite3.OperationalError: unable to open database file
```

**Solution:**
```yaml
# Render filesystem is ephemeral
# Use Render PostgreSQL instead

# Add PostgreSQL database:
# Dashboard → New → PostgreSQL
# Connect to your web service
```

### **Problem 4: Environment Variables Not Set**

**Error:**
```
KeyError: 'SECRET_KEY'
```

**Solution:**
```
1. Render Dashboard → Environment tab
2. Add SECRET_KEY
3. Click Save Changes
4. Wait for auto-redeploy
```

### **Problem 5: Slow Cold Start**

**Issue:**
First request after inactivity is slow

**Solution:**
```
Free tier spins down after 15 min inactivity
Upgrade to paid plan ($7/month) for always-on
Or use cron job to ping every 10 minutes
```

---

## 📊 RENDER PRICING

### **Free Tier**

- ✅ 750 hours/month
- ✅ No sleep (always on)
- ✅ 512 MB RAM
- ✅ Shared CPU
- ✅ Free SSL
- ⚠️ Spins down after 15 min inactivity

### **Starter ($7/month)**

- ✅ Always on (no spin down)
- ✅ 512 MB RAM
- ✅ Shared CPU
- ✅ Custom domains

### **Standard ($25/month)**

- ✅ 2 GB RAM
- ✅ Dedicated CPU
- ✅ Better performance

**More info:** https://render.com/pricing

---

## 🎯 DEPLOYMENT CHECKLIST

- [ ] Render account created
- [ ] Repository connected
- [ ] render.yaml configured
- [ ] build.sh executable
- [ ] requirements.txt correct
- [ ] Environment variables set
- [ ] Service created
- [ ] First deployment successful
- [ ] App accessible via URL
- [ ] GitHub secrets configured (optional)
- [ ] Auto-deploy working
- [ ] Logs checked

---

## 🔗 USEFUL LINKS

- **Render Homepage:** https://render.com
- **Render Docs:** https://render.com/docs
- **Python on Render:** https://render.com/docs/deploy-flask
- **Render Dashboard:** https://dashboard.render.com
- **Render Status:** https://status.render.com
- **Render Community:** https://community.render.com

---

## ✅ QUICK REFERENCE

```bash
# Deploy từ GitHub
git push origin main
# → Auto-deploy on Render

# Manual deploy via API
curl -X POST "https://api.render.com/v1/services/SERVICE_ID/deploys" \
  -H "Authorization: Bearer API_KEY"

# View logs
# Dashboard → Logs tab

# Rollback
# Dashboard → Events → Rollback

# Environment variables
# Dashboard → Environment tab
```

---

<div align="center">

## 🎉 READY TO DEPLOY ON RENDER!

**Advantages over Heroku:**
- ✅ Better free tier
- ✅ No sleep
- ✅ Faster builds
- ✅ Modern platform

**Next Steps:**
1. Create Render account
2. Connect GitHub repo
3. Deploy!

</div>

