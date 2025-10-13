# ✅ TEST DEPLOYMENT CHECKLIST

**Service:** https://fb-news-rlrs.onrender.com  
**Date:** 2025-10-13  
**Status:** 🔄 Redeploying with fix

---

## 📋 PRE-DEPLOYMENT CHECKLIST

- [x] ✅ render.yaml updated (buildCommand uses build.sh)
- [x] ✅ build.sh exists and initializes database
- [x] ✅ Code pushed to GitHub (cicd-pipeline branch)
- [x] ✅ GitHub Actions triggered
- [ ] ⏳ Render auto-deploy triggered (check dashboard)

---

## 🔍 STEP 1: MONITOR RENDER DEPLOYMENT

### **A. Open Render Dashboard**
```
URL: https://dashboard.render.com/
```

### **B. Check Service Status**
1. Click on service: **fb-news**
2. Check status indicator:
   - 🔄 **Deploying** (yellow) - In progress
   - ✅ **Live** (green) - Success
   - ❌ **Failed** (red) - Error

### **C. Monitor Build Logs**
Click **"Logs"** tab and watch for:

**Expected logs:**
```
==> Building...
==> Running build command: chmod +x build.sh && ./build.sh
==> Collecting Flask==3.0.0
==> Collecting requests==2.31.0
==> Collecting python-dotenv==1.0.0
==> Collecting Flask-Login==0.6.3
==> Collecting Werkzeug==3.0.1
==> Collecting gunicorn==21.2.0
==> Installing collected packages: ...
==> Successfully installed Flask-3.0.0 requests-2.31.0 ...
==> Build completed successfully!
==> Starting service...
==> [INFO] Starting gunicorn 21.2.0
==> [INFO] Listening at: http://0.0.0.0:10000
==> [INFO] Booting worker with pid: 20
==> Service is live!
```

**Key indicators:**
- ✅ "chmod +x build.sh && ./build.sh" executed
- ✅ "Build completed successfully!"
- ✅ "Listening at: http://0.0.0.0:10000"
- ✅ "Service is live!"
- ✅ NO "no such table" errors

---

## 🔍 STEP 2: TEST SERVICE URL

### **A. Test Homepage**

```powershell
# Test with curl
curl https://fb-news-rlrs.onrender.com

# Expected: HTML response (status 200)
```

**Or open in browser:**
```
https://fb-news-rlrs.onrender.com
```

**Expected Result:**
- ✅ Page loads successfully
- ✅ Shows statistics: "Leagues: X, Teams: Y, Players: Z, Matches: W"
- ✅ No error messages
- ✅ No "no such table: leagues" error

**Screenshot checklist:**
- [ ] ✅ Homepage displays
- [ ] ✅ Navigation bar visible
- [ ] ✅ Statistics section shows
- [ ] ✅ Footer displays

---

### **B. Test API Endpoints**

```powershell
# 1. Test leagues API
curl https://fb-news-rlrs.onrender.com/api/leagues

# Expected: [] (empty array) or JSON array of leagues
# NOT: Error 500 or "no such table"

# 2. Test teams API
curl https://fb-news-rlrs.onrender.com/api/teams

# Expected: [] (empty array) or JSON array of teams

# 3. Test players API
curl https://fb-news-rlrs.onrender.com/api/players

# Expected: [] (empty array) or JSON array of players

# 4. Test matches API
curl https://fb-news-rlrs.onrender.com/api/matches

# Expected: [] (empty array) or JSON array of matches
```

**API Response Checklist:**
- [ ] ✅ /api/leagues returns JSON (not error)
- [ ] ✅ /api/teams returns JSON (not error)
- [ ] ✅ /api/players returns JSON (not error)
- [ ] ✅ /api/matches returns JSON (not error)

---

### **C. Test Authentication**

**1. Test Register Page:**
```
URL: https://fb-news-rlrs.onrender.com/register
```
- [ ] ✅ Register form displays
- [ ] ✅ Can fill in username, email, password
- [ ] ✅ Submit button works

**2. Test Login Page:**
```
URL: https://fb-news-rlrs.onrender.com/login
```
- [ ] ✅ Login form displays
- [ ] ✅ Can enter credentials
- [ ] ✅ Submit button works

**3. Create Test User:**
```
Username: testuser
Email: test@example.com
Password: Test123!
```
- [ ] ✅ Registration successful
- [ ] ✅ Redirected to login or homepage
- [ ] ✅ Can login with new credentials

**4. Test Profile:**
```
URL: https://fb-news-rlrs.onrender.com/profile
```
- [ ] ✅ Profile page displays
- [ ] ✅ Shows user information
- [ ] ✅ Logout button works

---

## 🔍 STEP 3: TEST NAVIGATION

### **A. Test All Pages**

**1. Homepage:**
```
URL: https://fb-news-rlrs.onrender.com/
```
- [ ] ✅ Loads successfully
- [ ] ✅ Statistics display
- [ ] ✅ Links work

**2. Leagues Page:**
```
URL: https://fb-news-rlrs.onrender.com/leagues
```
- [ ] ✅ Page loads
- [ ] ✅ Shows leagues list (or empty state)

**3. Teams Page:**
```
URL: https://fb-news-rlrs.onrender.com/teams
```
- [ ] ✅ Page loads
- [ ] ✅ Shows teams list (or empty state)

**4. Players Page:**
```
URL: https://fb-news-rlrs.onrender.com/players
```
- [ ] ✅ Page loads
- [ ] ✅ Shows players list (or empty state)

---

## 🔍 STEP 4: CHECK LOGS FOR ERRORS

### **A. Render Logs**

**Check for common errors:**
```
❌ "no such table: leagues" - Database not initialized
❌ "Port scan timeout" - App not starting
❌ "Application failed to start" - Code error
❌ "ModuleNotFoundError" - Missing dependency
```

**Expected: NO errors, only INFO logs:**
```
✅ [INFO] Starting gunicorn
✅ [INFO] Listening at: http://0.0.0.0:10000
✅ [INFO] Booting worker with pid: X
```

---

## 🔍 STEP 5: PERFORMANCE TEST

### **A. Response Time**

```powershell
# Test response time
Measure-Command { curl https://fb-news-rlrs.onrender.com }

# Expected: < 5 seconds (first request after sleep)
# Expected: < 1 second (subsequent requests)
```

### **B. Cold Start Test**

**If service was sleeping:**
1. Wait 15+ minutes (service sleeps)
2. Access URL again
3. Measure wake-up time

**Expected:**
- ⏱️ Cold start: 30-60 seconds
- ⏱️ Warm requests: < 1 second

---

## 🔍 STEP 6: VERIFY AUTO-DEPLOYMENT

### **A. Check GitHub Actions**

```
URL: https://github.com/thangnt04-scr/FB-News/actions
```

**Verify:**
- [ ] ✅ Latest workflow run completed
- [ ] ✅ All jobs passed (green)
- [ ] ✅ Deploy job executed (if secrets configured)

### **B. Check Render Events**

**Render Dashboard → Events tab:**
- [ ] ✅ Shows latest deployment
- [ ] ✅ Triggered by: "Push to cicd-pipeline"
- [ ] ✅ Status: Success

---

## 📊 FINAL CHECKLIST

### **Deployment Success Criteria:**

- [ ] ✅ Build logs show "Build completed successfully!"
- [ ] ✅ Service status is "Live" (green)
- [ ] ✅ Homepage loads without errors
- [ ] ✅ All API endpoints return JSON (not errors)
- [ ] ✅ Authentication works (register/login)
- [ ] ✅ No "no such table" errors in logs
- [ ] ✅ Port 10000 is listening
- [ ] ✅ GitHub Actions passed
- [ ] ✅ Auto-deployment working (if secrets configured)

---

## 🎯 IF ALL CHECKS PASS

```
🎉 DEPLOYMENT SUCCESSFUL!

Service URL: https://fb-news-rlrs.onrender.com
Status: ✅ Live and working
Database: ✅ Initialized
API: ✅ Functional
Auth: ✅ Working
```

**Next Steps:**
1. ✅ Add sample data (optional)
2. ✅ Configure GitHub Secrets for auto-deploy
3. ✅ Monitor service health
4. ✅ Share URL with users!

---

## ❌ IF CHECKS FAIL

### **Troubleshooting:**

**1. Check build logs for errors**
```
Render Dashboard → Logs tab → Look for ERROR or FAILED
```

**2. Verify build.sh executed**
```
Look for: "chmod +x build.sh && ./build.sh"
```

**3. Check database initialization**
```
Look for: "from db import init_db; init_db()"
```

**4. Force rebuild**
```
Render Dashboard → Settings → Clear build cache → Deploy
```

**5. Check environment variables**
```
PORT=10000
FLASK_ENV=production
PYTHON_VERSION=3.11.0
SECRET_KEY=(auto-generated)
```

---

## 📚 DOCUMENTATION

**For detailed troubleshooting:**
- `RENDER-DEPLOYMENT-FIX.md` - Fix details
- `RENDER-DEPLOYMENT-GUIDE.md` - Full deployment guide
- `QUICK-START.md` - Quick reference

---

**Last Updated:** 2025-10-13  
**Status:** ⏳ AWAITING REDEPLOY COMPLETION

