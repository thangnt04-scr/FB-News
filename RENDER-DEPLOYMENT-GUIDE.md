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

### **Test thủ công:**

```powershell
# 1. Commit và push code
git add .
git commit -m "Deploy to Render"
git push origin cicd-pipeline

# 2. Kiểm tra GitHub Actions
# Mở: https://github.com/thangnt04-scr/FB-News/actions

# 3. Đợi workflow hoàn thành (5-10 phút)

# 4. Kiểm tra Render Dashboard
# Mở: https://dashboard.render.com/

# 5. Test URL
curl https://fb-news-XXXX.onrender.com
# Hoặc mở browser
```

### **Test tự động (GitHub Actions):**

Workflow sẽ tự động:
1. ✅ Chạy security scans (Bandit, Safety, Trivy)
2. ✅ Build Docker image
3. ✅ Generate security reports
4. ✅ Trigger Render deployment (nếu có secrets)

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

