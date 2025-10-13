# 🚀 RENDER QUICK START - 5 PHÚT

## ✅ CHUẨN BỊ

Files đã sẵn sàng:
- ✅ render.yaml
- ✅ build.sh
- ✅ requirements.txt
- ✅ app.py
- ✅ Procfile

Code đã push lên GitHub:
- ✅ Branch: cicd-pipeline
- ✅ Commit: 2d17198

---

## 🚀 DEPLOY TRONG 5 BƯỚC

### **BƯỚC 1: Tạo Tài Khoản (1 phút)**

1. Visit: https://render.com
2. Click **"Get Started for Free"**
3. Click **"Sign up with GitHub"**
4. Authorize Render

### **BƯỚC 2: Tạo Web Service (2 phút)**

1. Click **"New +"** → **"Web Service"**
2. Find: **"FB-News"** → Click **"Connect"**
3. Configure:
   ```
   Name: football-app
   Region: Singapore
   Branch: cicd-pipeline
   Build Command: ./build.sh
   Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
   ```
4. Environment Variables:
   ```
   SECRET_KEY = [Generate]
   FLASK_ENV = production
   PYTHON_VERSION = 3.11.0
   ```
5. Plan: **Free**
6. Click **"Create Web Service"**

### **BƯỚC 3: Đợi Deploy (3-5 phút)**

Xem logs trong Render dashboard:
```
Building...
Installing dependencies...
Starting gunicorn...
✅ Deploy successful!
```

### **BƯỚC 4: Test App**

```powershell
# Thay YOUR_URL bằng URL từ Render
.\test-render-deployment.ps1 -RenderUrl "https://football-app.onrender.com"
```

### **BƯỚC 5: Setup Auto-Deploy (Optional)**

1. **Get Render API Key:**
   - Render → Account Settings → API Keys → Create

2. **Get Service ID:**
   - Dashboard → football-app → URL contains `srv-XXXXX`

3. **Add to GitHub:**
   - https://github.com/thangnt04-scr/FB-News/settings/secrets/actions
   - Add: `RENDER_API_KEY` và `RENDER_SERVICE_ID`

---

## ✅ DONE!

Your app is now live at:
```
https://football-app.onrender.com
```

Features:
- ✅ Free hosting
- ✅ Auto-deploy from GitHub
- ✅ Free SSL
- ✅ No sleep (always on)

---

## 🔗 LINKS

- **Render Dashboard:** https://dashboard.render.com
- **GitHub Actions:** https://github.com/thangnt04-scr/FB-News/actions
- **Full Guide:** RENDER-DEPLOYMENT-GUIDE.md

---

## ❓ TROUBLESHOOTING

### Build Failed?
```
Check: Render Dashboard → Logs
Common: Missing dependencies in requirements.txt
Fix: Update requirements.txt and redeploy
```

### App Not Starting?
```
Check: Start command is correct
Should be: gunicorn --bind 0.0.0.0:$PORT app:app
```

### 404 Error?
```
Check: App is deployed successfully
Check: URL is correct
Wait: First deploy may take 5 minutes
```

---

<div align="center">

## 🎉 READY TO DEPLOY!

**Time:** 5 minutes  
**Cost:** $0 (FREE)  
**Difficulty:** Easy

**Start now:** https://render.com

</div>

