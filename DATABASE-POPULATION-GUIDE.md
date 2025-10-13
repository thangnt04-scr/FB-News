# 📊 DATABASE POPULATION GUIDE

## ✅ GIẢI QUYẾT VẤN ĐỀ: WEB DEPLOY KHÔNG CÓ DỮ LIỆU

### **Vấn đề:**
- Web deploy thành công nhưng không có dữ liệu
- Database trống (0 leagues, 0 teams, 0 players, 0 matches)
- Docker container cũng mất data khi restart

### **Giải pháp:**
- Tạo script `populate_db.py` để fetch data từ football-data.org API
- Tự động populate database khi build/deploy
- Persist data trong Docker với volume mount

---

## 🚀 CÁC FILE MỚI

### **1. populate_db.py**
Script Python để populate database với dữ liệu thật từ API:

**Chức năng:**
- Fetch leagues từ API (Premier League, La Liga, Bundesliga, Serie A, Ligue 1, Champions League)
- Fetch 20 teams từ Premier League
- Fetch 25 players từ 5 teams (Arsenal, Chelsea, Man City, Man Utd, Tottenham)
- Fetch 20 recent matches từ Premier League
- Tạo admin user (username: admin, password: admin123)

**Sử dụng:**
```bash
python populate_db.py
```

**Output:**
```
🚀 POPULATING FOOTBALL DATABASE
📊 Populating Leagues...
  ✅ Added: Premier League
  ✅ Added: Primera Division
  ...
✅ DATABASE POPULATION COMPLETE!
📊 Total records inserted: 71
```

---

### **2. run-local-with-data.ps1**
Script PowerShell để chạy Flask app local với data:

**Chức năng:**
1. Xóa database cũ
2. Populate database mới với data từ API
3. Chạy Flask app trên http://localhost:5000

**Sử dụng:**
```powershell
.\run-local-with-data.ps1
```

---

### **3. run-docker-with-data.ps1**
Script PowerShell để chạy Docker container với data:

**Chức năng:**
1. Xóa database cũ
2. Populate database mới với data từ API
3. Build Docker image
4. Run Docker container với volume mount
5. Database được persist trong `footballinfor.db`

**Sử dụng:**
```powershell
.\run-docker-with-data.ps1
```

**Lợi ích:**
- ✅ Data được persist ngay cả khi container restart
- ✅ Volume mount: `./footballinfor.db:/app/footballinfor.db`
- ✅ Không mất data khi `docker-compose down` và `docker-compose up`

---

## 🔧 CẬP NHẬT build.sh

**Trước đây:**
```bash
#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python -c "from db import init_db; init_db()"

echo "Build completed successfully!"
```

**Bây giờ:**
```bash
#!/usr/bin/env bash
set -o errexit

echo "========================================="
echo "Starting build process..."
echo "========================================="

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "🔧 Initializing database..."
python -c "from db import init_db; init_db()"

# Populate database with football data
echo "📊 Populating database with football data..."
python populate_db.py

echo "========================================="
echo "✅ Build completed successfully!"
echo "========================================="
```

**Kết quả:**
- ✅ Render deployment sẽ tự động populate database khi build
- ✅ Mỗi lần deploy mới sẽ có data mới nhất từ API

---

## 📊 DỮ LIỆU ĐƯỢC POPULATE

### **Leagues (6 records):**
- Premier League (England)
- Primera Division / La Liga (Spain)
- Bundesliga (Germany)
- Serie A (Italy)
- Ligue 1 (France)
- UEFA Champions League (International)

### **Teams (20 records):**
- Arsenal FC
- Aston Villa FC
- Chelsea FC
- Everton FC
- Fulham FC
- Liverpool FC
- Manchester City FC
- Manchester United FC
- Newcastle United FC
- Sunderland AFC
- Tottenham Hotspur FC
- Wolverhampton Wanderers FC
- Burnley FC
- Leeds United FC
- Nottingham Forest FC
- Crystal Palace FC
- Brighton & Hove Albion FC
- Brentford FC
- West Ham United FC
- AFC Bournemouth

### **Players (25 records):**
- 5 players từ Arsenal FC
- 5 players từ Chelsea FC
- 5 players từ Manchester City FC
- 5 players từ Manchester United FC
- 5 players từ Tottenham Hotspur FC

### **Matches (20 records):**
- 20 recent finished matches từ Premier League
- Bao gồm: home team, away team, scores, date

### **Users (1 record):**
- Username: `admin`
- Password: `admin123`
- Role: `admin`

---

## 🔑 API CONFIGURATION

**API Provider:** football-data.org  
**API Key:** `714b8b0227af4ae7bec7cd46e191cf3a`  
**Base URL:** `https://api.football-data.org/v4`

**Rate Limiting:**
- Free tier: 10 requests per minute
- Script có built-in delay: 6 seconds giữa các requests
- Tự động retry nếu hit rate limit (429 error)

**Environment Variable:**
```bash
FOOTBALL_DATA_API_KEY=714b8b0227af4ae7bec7cd46e191cf3a
```

---

## 🐳 DOCKER VOLUME PERSISTENCE

**docker-compose.yml:**
```yaml
services:
  web:
    volumes:
      - ./footballinfor.db:/app/footballinfor.db  # ✅ Persist database
      - ./logs:/app/logs                          # ✅ Persist logs
```

**Lợi ích:**
- ✅ Database file được lưu trên host machine
- ✅ Không mất data khi container restart
- ✅ Có thể backup database dễ dàng
- ✅ Có thể inspect database với SQLite browser

---

## 🧪 TESTING

### **Test Local:**
```powershell
# Option 1: Chạy script tự động
.\run-local-with-data.ps1

# Option 2: Manual
Remove-Item footballinfor.db -Force
python populate_db.py
python app.py
```

**Verify:**
```bash
# Check database
python -c "import sqlite3; conn = sqlite3.connect('footballinfor.db'); cur = conn.cursor(); cur.execute('SELECT COUNT(*) FROM leagues'); print(f'Leagues: {cur.fetchone()[0]}'); cur.execute('SELECT COUNT(*) FROM teams'); print(f'Teams: {cur.fetchone()[0]}'); cur.execute('SELECT COUNT(*) FROM players'); print(f'Players: {cur.fetchone()[0]}'); cur.execute('SELECT COUNT(*) FROM matches'); print(f'Matches: {cur.fetchone()[0]}'); conn.close()"
```

**Expected Output:**
```
Leagues: 6
Teams: 20
Players: 25
Matches: 20
```

### **Test Docker:**
```powershell
# Option 1: Chạy script tự động
.\run-docker-with-data.ps1

# Option 2: Manual
Remove-Item footballinfor.db -Force
python populate_db.py
docker-compose down
docker-compose build
docker-compose up -d
docker-compose logs
```

**Verify:**
```bash
# Access container
docker exec -it football-app bash

# Check database inside container
python -c "import sqlite3; conn = sqlite3.connect('/app/footballinfor.db'); cur = conn.cursor(); cur.execute('SELECT COUNT(*) FROM leagues'); print(f'Leagues: {cur.fetchone()[0]}'); conn.close()"
```

---

## 🌐 RENDER DEPLOYMENT

**Automatic Population:**
1. Push code to GitHub
2. Render detects changes
3. Runs `build.sh`:
   - Install dependencies
   - Initialize database
   - **Populate database with API data** ✅
4. Starts app with Gunicorn

**Verify on Render:**
```bash
# Check Render logs
https://dashboard.render.com/

# Look for:
"📊 Populating database with football data..."
"✅ Added: Premier League"
"✅ Added: Arsenal FC"
"✅ DATABASE POPULATION COMPLETE!"
"📊 Total records inserted: 71"
```

**Test Deployed App:**
```bash
curl https://fb-news-rlrs.onrender.com
```

---

## 📝 COMMIT HISTORY

**Commit:** 9fe30d1  
**Message:** Add database population from API - Fix empty database issue

**Changes:**
- ✅ Created `populate_db.py` (270 lines)
- ✅ Updated `build.sh` (added population step)
- ✅ Created `run-local-with-data.ps1` (helper script)
- ✅ Created `run-docker-with-data.ps1` (helper script)
- ✅ Updated `footballinfor.db` (71 records)

**Total:** 5 files changed, 370 insertions(+), 1 deletion(-)

---

## 🎯 NEXT STEPS

1. **Monitor Render Deployment:**
   - Check logs for successful population
   - Verify data appears on website

2. **Test Website:**
   - Visit: https://fb-news-rlrs.onrender.com
   - Check leagues page
   - Check teams page
   - Check matches page

3. **Backup Database:**
   ```bash
   # Local backup
   cp footballinfor.db footballinfor.db.backup
   
   # Or use SQLite dump
   sqlite3 footballinfor.db .dump > backup.sql
   ```

---

## ✅ SUMMARY

**Problem Solved:**
- ✅ Empty database on deployment
- ✅ Empty database in Docker
- ✅ Data loss on container restart

**Solution Implemented:**
- ✅ API-based data population
- ✅ Automatic population on build
- ✅ Docker volume persistence
- ✅ Helper scripts for testing

**Result:**
- ✅ 71 records in database
- ✅ Real football data from API
- ✅ Data persists across restarts
- ✅ Automatic population on deploy

**🎊 DATABASE POPULATION COMPLETE! 🎊**

