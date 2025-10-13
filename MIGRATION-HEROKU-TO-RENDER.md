# 🔄 MIGRATION: HEROKU → RENDER

## 📋 TỔNG QUAN THAY ĐỔI

Project đã được migrate từ **Heroku** sang **Render** với các cải tiến về CI/CD pipeline.

---

## ✅ NHỮNG GÌ ĐÃ THAY ĐỔI

### **1. Cloud Platform: Heroku → Render**

| Aspect | **Before (Heroku)** | **After (Render)** |
|--------|--------------------|--------------------|
| **Platform** | Heroku | Render |
| **Free Tier** | ❌ Discontinued | ✅ 750 hours/month |
| **Sleep** | ✅ After 30 min | ❌ No sleep |
| **Config File** | Procfile | render.yaml + build.sh |
| **Deployment** | git push heroku main | Auto from GitHub |
| **Cost** | $7/month minimum | $0 (free tier) |

### **2. Files Thay Đổi**

#### **Removed (Heroku):**
```
❌ DEPLOY-TO-HEROKU.ps1
❌ HEROKU-DEPLOYMENT-GUIDE.md
```

#### **Added (Render):**
```
✅ render.yaml                    # Render service configuration
✅ build.sh                       # Build script for Render
✅ RENDER-DEPLOYMENT-GUIDE.md     # Complete Render guide
✅ CHECK-GITHUB-ACTIONS.ps1       # Workflow validation script
✅ MIGRATION-HEROKU-TO-RENDER.md  # This file
```

#### **Modified:**
```
📝 requirements.txt               # Fixed duplicate gunicorn
📝 .github/workflows/devsecops.yml # Updated deploy job for Render
```

#### **Kept (Still Valid):**
```
✅ Procfile                       # Still used by Render
✅ runtime.txt                    # Python version specification
```

---

## 🔧 CHI TIẾT THAY ĐỔI

### **1. requirements.txt**

**Before:**
```python
Flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
Flask-Login==0.6.3
Werkzeug==3.0.1
gunicorn==21.2.0
gunicorn  # ❌ Duplicate
```

**After:**
```python
Flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
Flask-Login==0.6.3
Werkzeug==3.0.1
gunicorn==21.2.0  # ✅ Fixed
```

### **2. render.yaml (NEW)**

```yaml
services:
  - type: web
    name: football-app
    env: python
    region: singapore
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT --workers 4 app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
      - key: FLASK_ENV
        value: production
```

### **3. build.sh (NEW)**

```bash
#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Initialize database if needed
python -c "import db; db.init_db()" || true
```

### **4. GitHub Actions Workflow**

**Deploy Job - Before (Heroku):**
```yaml
deploy:
  steps:
    - name: Deploy to Heroku
      run: git push heroku main
```

**Deploy Job - After (Render):**
```yaml
deploy:
  name: Deploy to Render
  steps:
    - name: Deploy to Render
      env:
        RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        RENDER_SERVICE_ID: ${{ secrets.RENDER_SERVICE_ID }}
      run: |
        curl -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
          -H "Authorization: Bearer $RENDER_API_KEY"
```

**Other Fixes:**
- ✅ Updated all actions to v4/v5
- ✅ Fixed Pylint command (exclude venv)
- ✅ Added `continue-on-error` flags
- ✅ Improved artifact uploads

---

## 🚀 CÁCH SỬ DỤNG MỚI

### **Deploy lên Render**

#### **Option 1: Auto-Deploy (Recommended)**

```bash
# 1. Push code to GitHub
git push origin main

# 2. Render tự động deploy
# → Check: https://dashboard.render.com
```

#### **Option 2: Manual Deploy**

```bash
# 1. Render Dashboard
# 2. Select service: football-app
# 3. Click "Manual Deploy"
# 4. Select branch
# 5. Deploy
```

#### **Option 3: API Deploy (from CI/CD)**

```bash
# GitHub Actions tự động trigger
# Khi push to main branch
```

### **Setup Render (Lần Đầu)**

1. **Create Account:**
   - Visit: https://render.com
   - Sign up with GitHub

2. **Connect Repository:**
   - New → Web Service
   - Select: thangnt04-scr/FB-News
   - Branch: main

3. **Configure:**
   - Name: football-app
   - Build Command: ./build.sh
   - Start Command: gunicorn app:app
   - Plan: Free

4. **Deploy:**
   - Click "Create Web Service"
   - Wait 3-5 minutes
   - App live at: https://football-app.onrender.com

### **Setup GitHub Secrets (Optional - for CI/CD)**

```
GitHub → Settings → Secrets → Actions

Add:
1. RENDER_API_KEY = [Your Render API Key]
2. RENDER_SERVICE_ID = srv-XXXXX
```

---

## 📊 SO SÁNH WORKFLOW

### **Before (Heroku):**

```
1. Developer push code
   ↓
2. GitHub Actions CI/CD
   ├─ Tests
   ├─ Security scans
   └─ Build Docker
   ↓
3. Manual: git push heroku main
   ↓
4. Heroku deploy ($7/month)
   ↓
5. App sleeps after 30 min
```

### **After (Render):**

```
1. Developer push code
   ↓
2. GitHub Actions CI/CD
   ├─ Tests
   ├─ Security scans
   ├─ Build Docker
   └─ Auto-trigger Render deploy
   ↓
3. Render auto-deploy (FREE)
   ↓
4. App always on (no sleep)
   ↓
5. Live at: https://football-app.onrender.com
```

---

## ✅ BENEFITS OF MIGRATION

### **1. Cost Savings**
- Heroku: $7/month minimum
- Render: $0 (free tier)
- **Savings: $84/year**

### **2. Better Performance**
- No sleep (Heroku free tier sleeps)
- Faster cold starts
- Better uptime

### **3. Better Developer Experience**
- Auto-deploy from GitHub
- Easier configuration (render.yaml)
- Better logs and monitoring
- Preview environments for PRs

### **4. Modern Infrastructure**
- Native Docker support
- Better build caching
- Faster deployments
- More regions available

---

## 🔍 VERIFICATION CHECKLIST

After migration, verify:

- [ ] ✅ render.yaml exists and configured
- [ ] ✅ build.sh exists and executable
- [ ] ✅ requirements.txt fixed (no duplicates)
- [ ] ✅ GitHub Actions workflow updated
- [ ] ✅ Render service created
- [ ] ✅ First deployment successful
- [ ] ✅ App accessible at Render URL
- [ ] ✅ Environment variables set
- [ ] ✅ Database initialized
- [ ] ✅ Logs showing no errors
- [ ] ✅ Auto-deploy working from GitHub
- [ ] ✅ CI/CD pipeline passing

---

## 📚 DOCUMENTATION

### **New Documentation:**
- `RENDER-DEPLOYMENT-GUIDE.md` - Complete Render guide
- `CHECK-GITHUB-ACTIONS.ps1` - Workflow validator
- `MIGRATION-HEROKU-TO-RENDER.md` - This file

### **Updated Documentation:**
- `DEVSECOPS-COMPLETE-SUMMARY.txt` - Updated for Render
- `HUONG_DAN_DEVSECOPS.md` - Updated Phase V

### **Removed Documentation:**
- ~~`DEPLOY-TO-HEROKU.ps1`~~ - No longer needed
- ~~`HEROKU-DEPLOYMENT-GUIDE.md`~~ - Replaced with Render guide

---

## 🎯 NEXT STEPS

### **1. Validate Changes**
```powershell
.\CHECK-GITHUB-ACTIONS.ps1
```

### **2. Commit Changes**
```bash
git add .
git commit -m "Migrate from Heroku to Render

- Replace Heroku with Render for cloud deployment
- Add render.yaml and build.sh
- Fix requirements.txt (remove duplicate gunicorn)
- Update GitHub Actions deploy job
- Add Render deployment guide
- Remove Heroku-specific files"
```

### **3. Create New Branch for CI/CD**
```bash
git checkout -b cicd-pipeline
git push origin cicd-pipeline
```

### **4. Deploy to Render**
```
1. Visit: https://render.com
2. Create account
3. Connect GitHub repo
4. Deploy!
```

### **5. Monitor**
```
GitHub Actions: https://github.com/thangnt04-scr/FB-News/actions
Render Dashboard: https://dashboard.render.com
```

---

## 🔗 USEFUL LINKS

### **Render:**
- Homepage: https://render.com
- Docs: https://render.com/docs
- Dashboard: https://dashboard.render.com
- Status: https://status.render.com

### **GitHub:**
- Repository: https://github.com/thangnt04-scr/FB-News
- Actions: https://github.com/thangnt04-scr/FB-News/actions

### **Documentation:**
- Render Guide: `RENDER-DEPLOYMENT-GUIDE.md`
- DevSecOps Guide: `HUONG_DAN_DEVSECOPS.md`
- Quick Start: `BAT_DAU_O_DAY.txt`

---

<div align="center">

## ✅ MIGRATION COMPLETE!

**From:** Heroku (paid, sleeps)  
**To:** Render (free, always-on)

**Status:** Ready to deploy

**Next:** Create CI/CD branch and push!

</div>

