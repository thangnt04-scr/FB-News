# 🚀 HƯỚNG DẪN DEPLOY LÊN RENDER

## 📋 CHUẨN BỊ

### ✅ Đã có:
- GitHub Repository: https://github.com/thangnt04-scr/FB-News
- Branch: `cicd-pipeline`
- File `render.yaml` (cấu hình service)
- File `build.sh` (build script)
- Tài khoản Render

### 🔑 Thông tin cần thiết:
- Render API Key: `rnd_rb9fxHXk9NQPpxcpCCBhiwr2RyjF`

---

## 🎯 BƯỚC 1: TẠO WEB SERVICE TRÊN RENDER

### **Cách 1: Qua Dashboard (Khuyến nghị)**

1. **Đăng nhập Render:**
   - URL: https://dashboard.render.com/

2. **Tạo Web Service mới:**
   - Click **"New +"** → **"Web Service"**

3. **Connect GitHub Repository:**
   - Chọn repository: `thangnt04-scr/FB-News`
   - Click **"Connect"**

4. **Cấu hình Service:**
   ```
   Name: fb-news
   Region: Singapore
   Branch: cicd-pipeline
   Runtime: Python 3
   Build Command: ./build.sh
   Start Command: gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120 app:app
   Plan: Free
   ```

5. **Environment Variables:**
   ```
   PYTHON_VERSION = 3.11.0
   FLASK_ENV = production
   SECRET_KEY = (auto-generated)
   PORT = 10000
   ```

6. **Click "Create Web Service"**

7. **Đợi deployment (2-3 phút)**

8. **Lấy Service URL:**
   - Sẽ có dạng: `https://fb-news-XXXX.onrender.com`

---

### **Cách 2: Tự động với render.yaml**

Render sẽ tự động detect file `render.yaml` và apply cấu hình.

Chỉ cần:
1. Push code lên branch `cicd-pipeline`
2. Connect repository trên Render Dashboard
3. Render sẽ tự động đọc `render.yaml` và deploy

---

## 🎯 BƯỚC 2: CẤU HÌNH GITHUB SECRETS

Để enable auto-deployment từ GitHub Actions:

1. **Mở GitHub Repository Settings:**
   - URL: https://github.com/thangnt04-scr/FB-News/settings/secrets/actions

2. **Thêm Secrets:**

   **Secret 1: RENDER_API_KEY**
   ```
   Name: RENDER_API_KEY
   Value: rnd_rb9fxHXk9NQPpxcpCCBhiwr2RyjF
   ```

   **Secret 2: RENDER_SERVICE_ID**
   ```
   Name: RENDER_SERVICE_ID
   Value: <service-id-from-render-dashboard>
   ```

3. **Lấy Service ID:**
   - Mở Render Dashboard
   - Click vào service `fb-news`
   - URL sẽ có dạng: `https://dashboard.render.com/web/srv-XXXXXXXXXX`
   - Copy phần `srv-XXXXXXXXXX` → đây là Service ID

---

## 🎯 BƯỚC 3: TEST DEPLOYMENT

### **A. Kiểm tra Build Logs trên Render**

**Sau khi tạo service, kiểm tra logs:**

1. **Mở Render Dashboard:**
   ```
   https://dashboard.render.com/
   ```

2. **Click vào service `fb-news`**

3. **Click tab "Logs"**

4. **Kiểm tra build process:**
   ```
   Expected logs:
   ==> Building...
   ==> Running build command: chmod +x build.sh && ./build.sh
   ==> Installing dependencies...
   ==> Collecting Flask==3.0.0
   ==> Collecting requests==2.31.0
   ==> ...
   ==> Initializing database...
   ==> Build completed successfully!
   ==> Starting service...
   ==> [INFO] Starting gunicorn 21.2.0
   ==> [INFO] Listening at: http://0.0.0.0:10000
   ==> Service is live!
   ```

5. **Nếu thấy lỗi:**
   ```
   ERROR: no such table: leagues
   ```
   → Database chưa được init. Cần redeploy với build.sh đúng.

---

### **B. Test Service URL**

**Sau khi service live:**

```powershell
# 1. Lấy Service URL từ Render Dashboard
# URL có dạng: https://fb-news-XXXX.onrender.com

# 2. Test homepage
curl https://fb-news-k8za.onrender.com

# Expected: HTML response với status 200

# 3. Test trong browser
start https://fb-news-k8za.onrender.com
```

**Expected Result:**
- ✅ Trang chủ hiển thị
- ✅ Có thống kê: Leagues, Teams, Players, Matches
- ✅ Không có lỗi "no such table"

---

### **C. Test API Endpoints**

```powershell
# Test leagues API
curl https://fb-news-k8za.onrender.com/api/leagues

# Expected: JSON array of leagues
# [{"id": 1, "name": "Premier League", ...}, ...]

# Test teams API
curl https://fb-news-k8za.onrender.com/api/teams

# Expected: JSON array of teams

# Test players API
curl https://fb-news-k8za.onrender.com/api/players

# Expected: JSON array of players
```

---

### **D. Test Authentication**

```powershell
# 1. Mở trang login
start https://fb-news-k8za.onrender.com/login

# 2. Thử đăng ký user mới
# Click "Register" → Điền form → Submit

# 3. Thử đăng nhập
# Username: test
# Password: test123

# 4. Kiểm tra profile
# Sau khi login → Click "Profile"
```

---

### **E. Troubleshooting Common Errors**

#### **Error 1: "no such table: leagues"**

**Nguyên nhân:** Database chưa được khởi tạo

**Giải pháp:**
```bash
# 1. Kiểm tra build.sh có được chạy không
# Xem logs: "Running build command: chmod +x build.sh && ./build.sh"

# 2. Nếu không thấy, update render.yaml:
buildCommand: chmod +x build.sh && ./build.sh

# 3. Trigger manual deploy:
# Render Dashboard → Service → Manual Deploy → Deploy latest commit
```

#### **Error 2: "Port scan timeout"**

**Nguyên nhân:** App không start được hoặc crash

**Giải pháp:**
```bash
# 1. Kiểm tra logs để tìm lỗi
# 2. Thường do:
#    - Database init failed
#    - Missing dependencies
#    - Wrong PORT environment variable

# 3. Verify environment variables:
PORT=10000
FLASK_ENV=production
PYTHON_VERSION=3.11.0
```

#### **Error 3: "Application failed to start"**

**Nguyên nhân:** Lỗi trong code hoặc dependencies

**Giải pháp:**
```bash
# 1. Kiểm tra requirements.txt
# 2. Test local trước:
docker-compose up -d
curl http://localhost:5000

# 3. Nếu local OK, kiểm tra Render logs
```

---

### **F. Verify Deployment Success**

**Checklist:**
- [ ] ✅ Build logs không có lỗi
- [ ] ✅ Service status: "Live" (màu xanh)
- [ ] ✅ Homepage accessible
- [ ] ✅ API endpoints return data
- [ ] ✅ Login/Register works
- [ ] ✅ No "no such table" errors

**Nếu tất cả ✅:**
```
🎉 DEPLOYMENT SUCCESSFUL!
Service URL: https://fb-news-k8za.onrender.com
```

---

### **G. Monitor Service**

**Render Dashboard:**
```
1. Metrics tab:
   - CPU usage
   - Memory usage
   - Request count

2. Logs tab:
   - Real-time logs
   - Error tracking

3. Events tab:
   - Deployment history
   - Service restarts
```

**Free Tier Notes:**
- ⚠️ Service sleeps after 15 min inactivity
- ⚠️ Cold start: 30-60 seconds
- ⚠️ SQLite data lost on restart (use PostgreSQL for persistence)

---

### **H. Test Auto-Deployment (After GitHub Secrets Setup)**

```powershell
# 1. Make a small change
echo "# Test auto-deploy" >> README.md

# 2. Commit and push
git add README.md
git commit -m "Test auto-deployment"
git push origin cicd-pipeline

# 3. Check GitHub Actions
# https://github.com/thangnt04-scr/FB-News/actions

# 4. Verify deployment triggered on Render
# Dashboard → Events tab → Should see new deployment

# 5. Wait for deployment to complete

# 6. Test URL again
curl https://fb-news-k8za.onrender.com
```

**Expected:**
- ✅ GitHub Actions runs successfully
- ✅ Render deployment triggered automatically
- ✅ Service updated with new code
- ✅ No downtime (rolling deployment)

---

## 🎯 BƯỚC 4: MONITOR & VERIFY

### **1. Kiểm tra Logs:**

**Render Dashboard:**
```
Dashboard → fb-news → Logs tab
```

**GitHub Actions:**
```
Repository → Actions → Latest workflow run
```

### **2. Kiểm tra Health:**

```powershell
# Test endpoint
curl https://fb-news-XXXX.onrender.com/

# Expected: HTML response with status 200
```

### **3. Kiểm tra Database:**

```powershell
# Test API endpoints
curl https://fb-news-XXXX.onrender.com/api/leagues
curl https://fb-news-XXXX.onrender.com/api/teams
```

---

## 📊 RENDER FREE TIER LIMITS

### **Giới hạn:**
- ✅ 750 hours/month (đủ cho 1 app 24/7)
- ✅ 512MB RAM
- ✅ Shared CPU
- ⚠️ Sleep sau 15 phút không hoạt động
- ⚠️ Cold start: 30-60 giây

### **Lưu ý về Database:**
- ⚠️ SQLite file sẽ bị mất khi restart
- ⚠️ Filesystem là ephemeral (tạm thời)
- 💡 Để lưu data lâu dài: Dùng PostgreSQL (Render có free tier)

---

## 🔧 TROUBLESHOOTING

### **Lỗi: Build failed**

**Nguyên nhân:** Thiếu dependencies hoặc lỗi trong `build.sh`

**Giải pháp:**
```bash
# Kiểm tra requirements.txt
cat requirements.txt

# Test build locally
chmod +x build.sh
./build.sh
```

### **Lỗi: Application failed to start**

**Nguyên nhân:** Port không đúng hoặc lỗi trong start command

**Giải pháp:**
```bash
# Kiểm tra PORT environment variable
echo $PORT

# Test start command locally
gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
```

### **Lỗi: 503 Service Unavailable**

**Nguyên nhân:** App đang sleep (free tier)

**Giải pháp:**
- Đợi 30-60 giây để app wake up
- Hoặc upgrade lên paid plan

---

## 📚 TÀI LIỆU THAM KHẢO

### **Render:**
- Dashboard: https://dashboard.render.com/
- Docs: https://render.com/docs
- API Docs: https://api-docs.render.com/

### **GitHub:**
- Repository: https://github.com/thangnt04-scr/FB-News
- Actions: https://github.com/thangnt04-scr/FB-News/actions

---

## ✅ CHECKLIST DEPLOYMENT

### **Trước khi deploy:**
- [x] ✅ Đã tạo `render.yaml`
- [x] ✅ Đã tạo `build.sh`
- [x] ✅ Đã test Docker build locally
- [x] ✅ Đã chạy security scans
- [x] ✅ Code đã push lên branch `cicd-pipeline`

### **Khi deploy:**
- [ ] ⏳ Tạo Web Service trên Render
- [ ] ⏳ Connect GitHub repository
- [ ] ⏳ Verify cấu hình
- [ ] ⏳ Click "Create Web Service"
- [ ] ⏳ Đợi deployment hoàn thành

### **Sau khi deploy:**
- [ ] ⏳ Lấy Service ID
- [ ] ⏳ Thêm GitHub Secrets (RENDER_API_KEY, RENDER_SERVICE_ID)
- [ ] ⏳ Test URL
- [ ] ⏳ Kiểm tra logs
- [ ] ⏳ Verify auto-deployment

---

## 🎉 HOÀN THÀNH

Sau khi hoàn thành tất cả các bước:

1. ✅ App đã deploy lên Render
2. ✅ Auto-deployment đã được cấu hình
3. ✅ CI/CD pipeline hoạt động
4. ✅ Security scans tự động chạy
5. ✅ Mọi thứ đã sẵn sàng cho production!

**Service URL:** `https://fb-news-XXXX.onrender.com`

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra Render logs
2. Kiểm tra GitHub Actions logs
3. Xem lại hướng dẫn này
4. Tham khảo Render documentation

---

**Good luck! 🚀**

