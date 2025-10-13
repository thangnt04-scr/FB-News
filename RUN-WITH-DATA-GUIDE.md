# 🚀 HƯỚNG DẪN CHẠY VỚI DỮ LIỆU

## ✅ VẤN ĐỀ ĐÃ GIẢI QUYẾT

**Trước đây:**
- ❌ Web deploy không có dữ liệu
- ❌ Docker container mất data khi restart
- ❌ Database trống (0 records)

**Bây giờ:**
- ✅ Tự động populate 71 records từ API
- ✅ Data persist trong Docker
- ✅ Render tự động populate khi deploy

---

## 🏃 1. CHẠY LOCAL VỚI DATA

### **Cách Nhanh (Khuyến nghị):**

```powershell
.\run-local-with-data.ps1
```

### **Cách Manual:**

```powershell
# Xóa database cũ
Remove-Item footballinfor.db -Force -ErrorAction SilentlyContinue

# Populate database
python populate_db.py

# Chạy app
python app.py
```

### **Truy cập:**
```
http://localhost:5000
```

---

## 🐳 2. CHẠY DOCKER VỚI DATA

### **Cách Nhanh (Khuyến nghị):**

```powershell
.\run-docker-with-data.ps1
```

### **Cách Manual:**

```powershell
# Xóa database cũ
Remove-Item footballinfor.db -Force

# Populate database
python populate_db.py

# Build và run Docker
docker-compose down
docker-compose build
docker-compose up -d

# Xem logs
docker-compose logs -f
```

### **Truy cập:**
```
http://localhost:5000
```

### **Lợi ích:**
- ✅ Data được persist với volume mount
- ✅ Không mất data khi restart container
- ✅ Database file: `./footballinfor.db`

---

## 🌐 3. DEPLOY LÊN RENDER

### **Push Code:**

```powershell
git add .
git commit -m "Your message"
git push origin cicd-pipeline
```

### **Render Tự Động:**

1. ✅ Detect changes từ GitHub
2. ✅ Run `build.sh`:
   - Install dependencies
   - Initialize database
   - **Populate 71 records từ API** ✅
3. ✅ Start app
4. ✅ Live tại: https://fb-news-rlrs.onrender.com

### **Monitor:**

```
https://dashboard.render.com/
```

**Check logs:**
```
📊 Populating database with football data...
  ✅ Added: Premier League
  ✅ Added: Arsenal FC
  ...
✅ DATABASE POPULATION COMPLETE!
📊 Total records inserted: 71
```

---

## 🔍 4. KIỂM TRA DATA

### **Check Records:**

```powershell
python -c "import sqlite3; conn = sqlite3.connect('footballinfor.db'); cur = conn.cursor(); cur.execute('SELECT COUNT(*) FROM leagues'); print(f'Leagues: {cur.fetchone()[0]}'); cur.execute('SELECT COUNT(*) FROM teams'); print(f'Teams: {cur.fetchone()[0]}'); cur.execute('SELECT COUNT(*) FROM players'); print(f'Players: {cur.fetchone()[0]}'); cur.execute('SELECT COUNT(*) FROM matches'); print(f'Matches: {cur.fetchone()[0]}'); conn.close()"
```

**Expected:**
```
Leagues: 6
Teams: 20
Players: 25
Matches: 20
```

### **View Data:**

```powershell
# Leagues
python -c "import sqlite3; conn = sqlite3.connect('footballinfor.db'); cur = conn.cursor(); cur.execute('SELECT name FROM leagues'); print('\n'.join([row[0] for row in cur.fetchall()])); conn.close()"

# Teams
python -c "import sqlite3; conn = sqlite3.connect('footballinfor.db'); cur = conn.cursor(); cur.execute('SELECT name FROM teams LIMIT 10'); print('\n'.join([row[0] for row in cur.fetchall()])); conn.close()"
```

---

## 👨‍💼 5. ADMIN LOGIN

**Credentials:**
```
Username: admin
Password: admin123
```

**Login URL:**
- Local: http://localhost:5000/login
- Deployed: https://fb-news-rlrs.onrender.com/login

⚠️ **Đổi password sau khi login lần đầu!**

---

## 📊 DỮ LIỆU

### **Leagues (6):**
- Premier League, La Liga, Bundesliga
- Serie A, Ligue 1, Champions League

### **Teams (20):**
- Arsenal, Chelsea, Man City, Man Utd
- Liverpool, Tottenham, Newcastle
- + 13 teams khác từ Premier League

### **Players (25):**
- 5 players từ mỗi team:
  - Arsenal, Chelsea, Man City, Man Utd, Tottenham

### **Matches (20):**
- 20 recent matches từ Premier League
- Có scores, dates, teams

---

## 🔧 TROUBLESHOOTING

### **Database trống?**

```powershell
Remove-Item footballinfor.db -Force
python populate_db.py
```

### **Docker không có data?**

```powershell
docker-compose down
Remove-Item footballinfor.db -Force
python populate_db.py
docker-compose up -d
```

### **API rate limit?**

- Đợi 1 phút rồi chạy lại
- Script có delay 6s giữa requests
- Free tier: 10 requests/minute

### **Render không có data?**

```powershell
# Trigger rebuild
git commit --allow-empty -m "Rebuild"
git push origin cicd-pipeline
```

---

## 📚 TÀI LIỆU

- **DATABASE-POPULATION-GUIDE.md** - Chi tiết về population
- **RENDER-DEPLOYMENT-GUIDE.md** - Deploy guide
- **FINAL-PROJECT-SUMMARY.md** - Tổng quan dự án

---

## ✅ CHECKLIST

- [ ] Local app có data (71 records)
- [ ] Docker app có data
- [ ] Data persist khi Docker restart
- [ ] Render deployment thành công
- [ ] Render app có data
- [ ] Admin login hoạt động

---

**🎊 CHÚC BẠN THÀNH CÔNG! 🎊**

