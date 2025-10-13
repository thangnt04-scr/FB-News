# 🚀 TẠO WEB SERVICE MỚI TRÊN RENDER

## 📋 CHUẨN BỊ

### **Đã có:**
- ✅ GitHub repo: https://github.com/thangnt04-scr/FB-News
- ✅ Branch: cicd-pipeline
- ✅ render.yaml (mới tạo)
- ✅ Code đã sửa lỗi

### **Cần:**
- ✅ Tài khoản Render (đã có)
- ✅ Render API Key: `rnd_rb9fxHXk9NQPpxcpCCBhiwr2RyjF`

---

## 🎯 BƯỚC 1: TẠO WEB SERVICE MỚI

### **Option A: Qua Dashboard (Dễ nhất)**

1. **Mở Render Dashboard:**
   - URL: https://dashboard.render.com/

2. **Click "New +" → "Web Service"**

3. **Connect GitHub Repository:**
   - Click "Connect account" (nếu chưa connect)
   - Hoặc chọn repo: `thangnt04-scr/FB-News`
   - Click "Connect"

4. **Configure Service:**
   ```
   Name: fb-news
   Region: Singapore
   Branch: cicd-pipeline
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   Plan: Free
   ```

5. **Environment Variables:**
   ```
   PYTHON_VERSION = 3.11.0
   PORT = 10000
   ```

6. **Click "Create Web Service"**

7. **Wait 2-3 minutes** for deployment

8. **Get Service URL:**
   - Will be: `https://fb-news-XXXX.onrender.com`

---

### **Option B: Qua API (Tự động)**

Tôi sẽ tạo script PowerShell để tự động tạo service:

---

## 🔧 BƯỚC 2: SCRIPT TỰ ĐỘNG TẠO SERVICE

Tạo file `create-render-service.ps1`:

```powershell
# Render API credentials
$RENDER_API_KEY = "rnd_rb9fxHXk9NQPpxcpCCBhiwr2RyjF"

# Service configuration
$serviceConfig = @{
    type = "web_service"
    name = "fb-news"
    ownerId = "YOUR_OWNER_ID"  # Get from dashboard
    repo = "https://github.com/thangnt04-scr/FB-News"
    branch = "cicd-pipeline"
    runtime = "python"
    plan = "free"
    region = "singapore"
    buildCommand = "pip install -r requirements.txt"
    startCommand = "python app.py"
    envVars = @(
        @{
            key = "PYTHON_VERSION"
            value = "3.11.0"
        },
        @{
            key = "PORT"
            value = "10000"
        }
    )
} | ConvertTo-Json -Depth 10

# Create service
$headers = @{
    "Authorization" = "Bearer $RENDER_API_KEY"
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod `
        -Uri "https://api.render.com/v1/services" `
        -Method POST `
        -Headers $headers `
        -Body $serviceConfig
    
    Write-Host "✅ Service created successfully!" -ForegroundColor Green
    Write-Host "Service ID: $($response.service.id)" -ForegroundColor Cyan
    Write-Host "URL: $($response.service.serviceDetails.url)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Failed to create service!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
}
```

---

## 📝 BƯỚC 3: LẤY OWNER ID

### **Cách 1: Qua Dashboard**
1. Mở: https://dashboard.render.com/
2. Click vào avatar (góc phải trên)
3. Click "Account Settings"
4. Copy "Owner ID"

### **Cách 2: Qua API**
```powershell
$headers = @{
    "Authorization" = "Bearer rnd_rb9fxHXk9NQPpxcpCCBhiwr2RyjF"
}

$response = Invoke-RestMethod `
    -Uri "https://api.render.com/v1/owners" `
    -Headers $headers

$response.owners[0].id
```

---

## 🎯 KHUYẾN NGHỊ: DÙNG DASHBOARD

**Lý do:**
- ✅ Dễ hơn
- ✅ Trực quan
- ✅ Ít lỗi hơn
- ✅ Tự động connect GitHub
- ✅ Tự động detect render.yaml

**Chỉ mất 2 phút!**

---

## 📋 CHECKLIST TẠO SERVICE

### **Trước khi tạo:**
- [x] ✅ Đã xóa hết file cloud cũ
- [x] ✅ Đã tạo render.yaml mới
- [x] ✅ Đã sửa app.py (error handling)
- [x] ✅ Code đã push lên GitHub

### **Khi tạo service:**
- [ ] ⏳ Mở Render Dashboard
- [ ] ⏳ Click "New +" → "Web Service"
- [ ] ⏳ Connect GitHub repo
- [ ] ⏳ Chọn branch: cicd-pipeline
- [ ] ⏳ Verify config (auto-detect từ render.yaml)
- [ ] ⏳ Click "Create Web Service"

### **Sau khi tạo:**
- [ ] ⏳ Wait for deployment (2-3 min)
- [ ] ⏳ Get service URL
- [ ] ⏳ Test app
- [ ] ⏳ Save service ID

---

## 🔗 LINKS

### **Render:**
- **Dashboard:** https://dashboard.render.com/
- **New Service:** https://dashboard.render.com/select-repo?type=web
- **API Docs:** https://api-docs.render.com/

### **GitHub:**
- **Repository:** https://github.com/thangnt04-scr/FB-News
- **Branch:** https://github.com/thangnt04-scr/FB-News/tree/cicd-pipeline

---

## 🎯 SAU KHI TẠO SERVICE

### **1. Lưu thông tin:**
```
Service Name: fb-news
Service ID: srv-XXXXXXXXXX (copy từ dashboard)
Service URL: https://fb-news-XXXX.onrender.com
Region: Singapore
Plan: Free
```

### **2. Test deployment:**
```powershell
# Test URL
curl https://fb-news-XXXX.onrender.com

# Or open browser
start https://fb-news-XXXX.onrender.com
```

### **3. Monitor logs:**
```
Dashboard → Your Service → Logs tab
```

### **4. Setup auto-deploy:**
```
Dashboard → Your Service → Settings
→ Auto-Deploy: Yes (default)
→ Branch: cicd-pipeline
```

---

## 💡 LƯU Ý

### **Free Tier Limits:**
- ✅ 750 hours/month (enough for 1 app 24/7)
- ✅ 512MB RAM
- ✅ Shared CPU
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ Cold start: 30-60 seconds

### **Database:**
- ⚠️ SQLite file will be lost on restart
- ⚠️ Render filesystem is ephemeral
- 💡 For persistent data: Use PostgreSQL (free tier available)

### **Auto-Deploy:**
- ✅ Enabled by default
- ✅ Deploys on every push to branch
- ✅ Can disable in settings

---

<div align="center">

## 🚀 BẮT ĐẦU NGAY

**Step 1:** Mở Dashboard  
https://dashboard.render.com/

**Step 2:** Click "New +" → "Web Service"

**Step 3:** Connect repo `thangnt04-scr/FB-News`

**Step 4:** Click "Create Web Service"

**Step 5:** Wait 2-3 minutes

**Step 6:** ✅ DONE!

</div>

