# ☁️ HEROKU DEPLOYMENT GUIDE - FOOTBALL APP

## 📋 MỤC LỤC

1. [Heroku là gì?](#heroku-là-gì)
2. [Chuẩn bị](#chuẩn-bị)
3. [Cài đặt Heroku CLI](#cài-đặt-heroku-cli)
4. [Deploy bằng Script](#deploy-bằng-script)
5. [Deploy thủ công](#deploy-thủ-công)
6. [Kiểm tra và quản lý](#kiểm-tra-và-quản-lý)
7. [Troubleshooting](#troubleshooting)

---

## 🌐 HEROKU LÀ GÌ?

**Heroku** là một Platform as a Service (PaaS) cho phép bạn:
- ✅ Deploy ứng dụng web lên cloud
- ✅ Tự động scale resources
- ✅ Quản lý database, logs, monitoring
- ✅ Free tier cho testing/demo
- ✅ Hỗ trợ Python, Node.js, Ruby, Java, PHP, Go

**Website:** https://www.heroku.com

---

## 🔧 CHUẨN BỊ

### Files Cần Thiết (✅ Đã có sẵn)

```
D:\Football\
├── Procfile                    # Heroku process definition
├── runtime.txt                 # Python version
├── requirements.txt            # Python dependencies
├── app.py                      # Flask application
└── .env                        # Environment variables (local only)
```

### Kiểm tra Files

#### 1. **Procfile**
```bash
cat Procfile
```
Nội dung:
```
web: gunicorn --bind 0.0.0.0:$PORT app:app
```

#### 2. **runtime.txt**
```bash
cat runtime.txt
```
Nội dung:
```
python-3.11.0
```

#### 3. **requirements.txt**
```bash
cat requirements.txt
```
Phải có:
```
Flask==3.0.0
gunicorn==21.2.0
requests==2.31.0
python-dotenv==1.0.0
Flask-Login==0.6.3
Werkzeug==3.0.1
```

---

## 📥 CÀI ĐẶT HEROKU CLI

### **Windows (PowerShell)**

#### Option 1: Download Installer
```powershell
# 1. Download từ:
https://devcenter.heroku.com/articles/heroku-cli

# 2. Chạy installer
# 3. Restart terminal
```

#### Option 2: Chocolatey
```powershell
# Nếu đã có Chocolatey
choco install heroku-cli -y

# Restart terminal
```

#### Option 3: Scoop
```powershell
scoop install heroku-cli
```

### **Verify Installation**
```powershell
heroku --version
# Output: heroku/8.x.x win32-x64 node-v18.x.x
```

---

## 🚀 DEPLOY BẰNG SCRIPT (KHUYẾN NGHỊ)

### **Cách 1: Sử dụng Script Tự Động**

```powershell
# Chạy script deploy
.\DEPLOY-TO-HEROKU.ps1
```

**Script sẽ tự động:**
1. ✅ Check Heroku CLI
2. ✅ Login to Heroku
3. ✅ Create app với tên ngẫu nhiên
4. ✅ Add Heroku remote
5. ✅ Set environment variables
6. ✅ Deploy code
7. ✅ Scale dynos
8. ✅ Open app in browser

**Thời gian:** ~5 phút

---

## 🛠️ DEPLOY THỦ CÔNG

### **Bước 1: Login to Heroku**

```powershell
heroku login
```

Browser sẽ mở → Login với Heroku account

### **Bước 2: Create Heroku App**

```powershell
# Tạo app với tên tự động
heroku create

# Hoặc tạo với tên cụ thể
heroku create football-app-demo
```

Output:
```
Creating app... done, ⬢ football-app-demo
https://football-app-demo.herokuapp.com/ | https://git.heroku.com/football-app-demo.git
```

### **Bước 3: Add Heroku Remote**

```powershell
# Nếu chưa có remote
heroku git:remote -a football-app-demo

# Verify
git remote -v
```

Output:
```
heroku  https://git.heroku.com/football-app-demo.git (fetch)
heroku  https://git.heroku.com/football-app-demo.git (push)
origin  https://github.com/thangnt04-scr/FB-News.git (fetch)
origin  https://github.com/thangnt04-scr/FB-News.git (push)
```

### **Bước 4: Set Environment Variables**

```powershell
# Set SECRET_KEY
heroku config:set SECRET_KEY="your-secret-key-here"

# Set Flask environment
heroku config:set FLASK_ENV=production

# Verify
heroku config
```

### **Bước 5: Deploy Code**

```powershell
# Deploy từ branch hiện tại
git push heroku devsecops-complete:main

# Hoặc từ main branch
git push heroku main
```

**Quá trình deploy:**
```
Counting objects: 100% (50/50), done.
Delta compression using up to 4 threads
Compressing objects: 100% (30/30), done.
Writing objects: 100% (50/50), 15.2 KiB | 5.07 MiB/s, done.

-----> Building on the Heroku-22 stack
-----> Using buildpack: heroku/python
-----> Python app detected
-----> Installing python-3.11.0
-----> Installing pip 23.x, setuptools 68.x and wheel 0.41.x
-----> Installing SQLite3
-----> Installing requirements with pip
       Collecting Flask==3.0.0
       Collecting gunicorn==21.2.0
       ...
       Successfully installed Flask-3.0.0 gunicorn-21.2.0 ...
-----> Discovering process types
       Procfile declares types -> web
-----> Compressing...
-----> Launching...
       Released v1
       https://football-app-demo.herokuapp.com/ deployed to Heroku
```

### **Bước 6: Scale Dynos**

```powershell
# Start 1 web dyno
heroku ps:scale web=1

# Check status
heroku ps
```

### **Bước 7: Open App**

```powershell
heroku open
```

Browser sẽ mở app: `https://football-app-demo.herokuapp.com/`

---

## 🔍 KIỂM TRA VÀ QUẢN LÝ

### **View Logs**

```powershell
# Real-time logs
heroku logs --tail

# Last 100 lines
heroku logs -n 100

# Filter by source
heroku logs --source app
```

### **Check App Status**

```powershell
# Dyno status
heroku ps

# App info
heroku apps:info

# Config vars
heroku config
```

### **Restart App**

```powershell
heroku restart
```

### **Run Commands**

```powershell
# Run Python shell
heroku run python

# Run bash
heroku run bash

# Run database migrations (if needed)
heroku run python migrate.py
```

### **View App in Dashboard**

```powershell
# Open Heroku dashboard
heroku dashboard
```

Or visit: https://dashboard.heroku.com/apps

---

## ❌ TROUBLESHOOTING

### **Problem 1: Application Error (H10)**

**Error:**
```
Application error
An error occurred in the application and your page could not be served.
```

**Solution:**
```powershell
# Check logs
heroku logs --tail

# Common causes:
# 1. Missing Procfile
# 2. Wrong Python version in runtime.txt
# 3. Missing dependencies in requirements.txt
# 4. Port binding issue

# Fix: Ensure Procfile has:
web: gunicorn --bind 0.0.0.0:$PORT app:app
```

### **Problem 2: Build Failed**

**Error:**
```
-----> Build failed
```

**Solution:**
```powershell
# Check requirements.txt
cat requirements.txt

# Ensure all dependencies are listed
# Ensure versions are compatible with Python 3.11

# Test locally first:
pip install -r requirements.txt
```

### **Problem 3: Database Error**

**Error:**
```
sqlite3.OperationalError: unable to open database file
```

**Solution:**
```powershell
# Heroku filesystem is ephemeral
# Use Heroku Postgres instead of SQLite

# Add Postgres addon
heroku addons:create heroku-postgresql:mini

# Update app.py to use DATABASE_URL
```

### **Problem 4: Slug Size Too Large**

**Error:**
```
Compiled slug size: 600M is too large (max is 500M)
```

**Solution:**
```powershell
# Add .slugignore file
echo "*.pyc" > .slugignore
echo "__pycache__/" >> .slugignore
echo "tests/" >> .slugignore
echo ".git/" >> .slugignore

# Commit and redeploy
git add .slugignore
git commit -m "Add .slugignore"
git push heroku main
```

### **Problem 5: Environment Variables Not Set**

**Error:**
```
KeyError: 'SECRET_KEY'
```

**Solution:**
```powershell
# Set missing environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set FLASK_ENV=production

# Verify
heroku config
```

---

## 📊 HEROKU PRICING

### **Free Tier (Eco Dynos)**

- ✅ 1000 dyno hours/month (free)
- ✅ Apps sleep after 30 min inactivity
- ✅ Good for testing/demo
- ⚠️ Cold start (slow first request)

### **Paid Tiers**

- **Basic ($7/month):** No sleep, custom domains
- **Standard ($25/month):** Better performance
- **Performance ($250+/month):** Production apps

**More info:** https://www.heroku.com/pricing

---

## 🎯 DEPLOYMENT CHECKLIST

- [ ] Heroku CLI installed
- [ ] Logged in to Heroku
- [ ] Procfile exists and correct
- [ ] runtime.txt has Python version
- [ ] requirements.txt has all dependencies
- [ ] Environment variables set
- [ ] Code committed to Git
- [ ] App created on Heroku
- [ ] Code pushed to Heroku
- [ ] Dynos scaled
- [ ] App accessible via URL
- [ ] Logs checked for errors

---

## 🔗 USEFUL LINKS

- **Heroku Dev Center:** https://devcenter.heroku.com/
- **Python on Heroku:** https://devcenter.heroku.com/categories/python-support
- **Heroku CLI:** https://devcenter.heroku.com/articles/heroku-cli
- **Deploying Python:** https://devcenter.heroku.com/articles/deploying-python
- **Heroku Dashboard:** https://dashboard.heroku.com/

---

## ✅ QUICK REFERENCE

```powershell
# Login
heroku login

# Create app
heroku create app-name

# Deploy
git push heroku main

# Logs
heroku logs --tail

# Restart
heroku restart

# Open app
heroku open

# Config
heroku config

# Status
heroku ps

# Run command
heroku run bash
```

---

<div align="center">

## 🎉 READY TO DEPLOY!

**Run the script:**
```powershell
.\DEPLOY-TO-HEROKU.ps1
```

**Or follow manual steps above**

</div>

