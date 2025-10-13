# ⚽ Football Information System

Hệ thống thông tin bóng đá toàn diện với chức năng đăng nhập phân quyền, quản lý dữ liệu từ các giải đấu hàng đầu thế giới.

## 🔒 DevSecOps Implementation

**Branch:** `cicd-pipeline`
**Status:** ✅ Production Ready

### **Security Features:**
- ✅ **SAST** - Bandit code scanning
- ✅ **Dependency Scan** - Safety vulnerability check
- ✅ **Container Scan** - Trivy image scanning
- ✅ **CI/CD Pipeline** - Automated security gates
- ✅ **Docker** - Production-ready with security hardening
- ✅ **Auto-Deploy** - Render.com integration

### **Quick Start:**
```bash
# Run security scans
.\run-devsecops-scans.ps1

# Build and run with Docker
docker-compose up -d

# View at http://localhost:5000
```

### **Documentation:**
- 📖 [Quick Start Guide](QUICK-START.md)
- 📖 [Render Deployment Guide](RENDER-DEPLOYMENT-GUIDE.md)
- 📖 [Complete DevSecOps Report](DEVSECOPS-COMPLETE-REPORT.md)
- 📖 [Implementation Summary](IMPLEMENTATION-SUMMARY.md)

### **Links:**
- 🔗 [GitHub Actions](https://github.com/thangnt04-scr/FB-News/actions)
- 🔗 [Security Reports](reports/)
- 🔗 [Live Demo](https://fb-news.onrender.com) (Coming soon)

## 🎯 Tính năng chính

### 👥 Cho tất cả người dùng:
- 🌍 Xem thông tin giải đấu, đội bóng, cầu thủ từ các giải hàng đầu
- 📊 Thống kê và dữ liệu chi tiết
- 🔍 Tìm kiếm nhanh
- 📱 Giao diện responsive, thân thiện

### 👑 Cho Admin:
- 🎛️ Dashboard quản lý toàn diện
- 👥 Quản lý người dùng (xem, sửa role, xóa)
- ➕ Thêm/sửa/xóa dữ liệu bóng đá
- 📈 Thống kê hệ thống
- 🔧 Cấu hình và bảo trì

### 👤 Cho User thường:
- 👀 Chỉ xem thông tin (read-only)
- 📋 Profile cá nhân
- 🚫 Không thể truy cập Dashboard
- 🚫 Không thể chỉnh sửa dữ liệu

## 📁 Cấu trúc dự án

```
Football/
├── 📄 app.py                 # Ứng dụng Flask chính
├── 🗄️ db.py                  # Database và functions
├── 🔐 auth.py                # Authentication module
├── 🛡️ decorators.py          # Custom decorators
├── 👤 create_admin.py        # Script tạo admin
├── 🔄 sync_all.py           # Sync dữ liệu từ API
├── 📋 requirements.txt       # Dependencies
├── 📖 README.md             # Hướng dẫn này
├── 📁 services/
│   └── 🌐 football_api.py   # API service
├── 📁 templates/
│   ├── 🏠 base.html         # Template chung
│   ├── 🏠 index.html        # Trang chủ
│   ├── 📊 dashboard.html    # Dashboard admin
│   ├── 🏆 league.html       # Trang giải đấu
│   ├── ⚽ team.html         # Trang đội bóng
│   ├── 👤 player.html       # Trang cầu thủ
│   └── 📁 auth/
│       ├── 🔑 login.html    # Đăng nhập
│       ├── 📝 register.html # Đăng ký
│       └── 👤 profile.html  # Profile
└── 📁 static/
    ├── 🎨 css/main.css      # CSS chính
    └── ⚡ js/main.js        # JavaScript chính
```

## 🚀 Hướng dẫn cài đặt và chạy

### Bước 1: Chuẩn bị môi trường

```bash
# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Kích hoạt virtual environment
# Trên Windows:
venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate
```

### Bước 2: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 3: Tạo tài khoản admin

```bash
python create_admin.py
```

**Output mong đợi:**
```
🚀 Tạo users mặc định...
==================================================
✅ Tạo admin user thành công!
   Username: admin
   Email: admin@football.com
   Password: admin123
   Role: admin

✅ Tạo test user thành công!
   Username: user
   Email: user@football.com
   Password: user123
   Role: user

==================================================
✅ Hoàn thành! Bạn có thể đăng nhập với:
   Admin: admin / admin123
   User:  user / user123
```

### Bước 4: Chạy ứng dụng

```bash
python app.py
```

**Output mong đợi:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
```

### Bước 5: Truy cập ứng dụng

🌐 **Mở trình duyệt và truy cập:** http://localhost:5000

## 🔐 Tài khoản mặc định

| Role | Username | Password | Quyền hạn |
|------|----------|----------|-----------|
| 👑 **Admin** | `admin` | `admin123` | Toàn quyền |
| 👤 **User** | `user` | `user123` | Chỉ xem |

## 🎮 Hướng dẫn sử dụng

### 🔑 Đăng nhập

1. Truy cập http://localhost:5000
2. Click **"Đăng nhập"** ở góc phải
3. Nhập username và password
4. Click **"Đăng nhập"**

### 👑 Sử dụng với tài khoản Admin

1. **Đăng nhập** với `admin` / `admin123`
2. **Dashboard:** Click "Dashboard" để quản lý users
3. **Quản lý Users:**
   - Xem danh sách tất cả users
   - Thay đổi role (Admin ↔ User)
   - Xóa users (trừ chính mình)
4. **Quản lý dữ liệu:** Có thể thêm/sửa/xóa dữ liệu bóng đá

### 👤 Sử dụng với tài khoản User

1. **Đăng nhập** với `user` / `user123`
2. **Xem dữ liệu:** Chỉ có thể xem thông tin
3. **Profile:** Click tên user để xem profile
4. **Giới hạn:** Không thể truy cập Dashboard

### 📝 Đăng ký tài khoản mới

1. Click **"Đăng ký"** ở góc phải
2. Điền thông tin:
   - Tên đăng nhập
   - Email
   - Mật khẩu
   - Xác nhận mật khẩu
3. Click **"Đăng ký"**
4. Đăng nhập với tài khoản mới

## 📊 Database Schema

Hệ thống sử dụng **SQLite** với các bảng:

```sql
-- Bảng người dùng
users (id, username, email, password_hash, role, created_at)

-- Bảng giải đấu
leagues (id, name, country_code, external_id)

-- Bảng đội bóng
teams (id, league_id, name, short_name, founded_year, stadium, external_id)

-- Bảng cầu thủ
players (id, team_id, name, nationality, position, shirt_number, birthdate, height_cm, weight_kg, external_id)

-- Bảng trận đấu
matches (id, league_id, season, match_date, home_team_id, away_team_id, home_score, away_score, external_id)
```

## 🔧 API Endpoints

### 🌐 Public Endpoints (Không cần đăng nhập)
```
GET  /                    # Trang chủ
GET  /login              # Form đăng nhập
POST /login              # Xử lý đăng nhập
GET  /register           # Form đăng ký
POST /register           # Xử lý đăng ký
GET  /api/leagues        # Danh sách giải đấu
GET  /api/leagues/{id}/teams  # Đội bóng trong giải
GET  /api/teams/{id}     # Chi tiết đội bóng
GET  /api/teams/{id}/players  # Cầu thủ của đội
GET  /api/players/{id}   # Chi tiết cầu thủ
```

### 🔐 Protected Endpoints (Cần đăng nhập)
```
GET  /profile            # Profile cá nhân
GET  /logout             # Đăng xuất
```

### 👑 Admin Only Endpoints
```
GET  /dashboard          # Dashboard admin
GET  /api/admin/users    # Danh sách users
PUT  /api/admin/users/{id}/role  # Cập nhật role
DELETE /api/admin/users/{id}     # Xóa user
```

## 🛡️ Bảo mật

- ✅ **Password Hashing:** Sử dụng Werkzeug để hash password
- ✅ **Session Management:** Flask-Login quản lý session
- ✅ **Role-based Access:** Phân quyền rõ ràng Admin/User
- ✅ **CSRF Protection:** Flask tự động bảo vệ
- ✅ **Input Validation:** Kiểm tra dữ liệu đầu vào

## 🎨 Giao diện

- 🎨 **Bootstrap 5:** Giao diện hiện đại, responsive
- 📱 **Mobile-friendly:** Tối ưu cho mọi thiết bị
- 🎯 **User Experience:** Dễ sử dụng, trực quan
- 🌈 **Icons:** Font Awesome icons
- ⚡ **Fast Loading:** Tối ưu hiệu suất

## 🔄 Sync dữ liệu từ API

Để đồng bộ dữ liệu từ football-data.org:

1) Cấu hình API key (không hard-code trong mã nguồn nữa):

```bash
# Tạo file .env (cùng thư mục với dự án)
echo "FOOTBALL_DATA_API_KEY=your_api_key_here" > .env
```

2) Chạy sync:

```bash
python sync_all.py
# Tuỳ chọn: chỉ sync cầu thủ cho các đội đã có external_id
python sync_players.py
```

Gợi ý: Nếu lệnh `python` không tồn tại trên Linux/macOS, hãy dùng `python3`.

## 🐛 Troubleshooting

### Lỗi thường gặp:

1. **"Module not found"**
   ```bash
   pip install -r requirements.txt
   ```

2. **"Database locked"**
   - Đảm bảo không có process nào đang sử dụng database
   - Restart ứng dụng

3. **"Port 5000 already in use"**
   ```bash
   # Thay đổi port trong app.py
   app.run(debug=True, port=5001)
   ```

4. **"Admin user already exists"**
   - Chạy lại `python create_admin.py` sẽ bỏ qua user đã tồn tại

5. **Thiếu dữ liệu/thiếu đội/cầu thủ**
   - Dùng các script dữ liệu sau (tuỳ tình huống):
     - `add_sample_data.py`: thêm bộ dữ liệu mẫu tối thiểu (leagues/teams/players/matches)
     - `add_important_teams.py`: bổ sung nhanh các đội lớn (La Liga, Bundesliga, Serie A)
     - `add_missing_teams.py`: thêm đầy đủ các đội còn thiếu cho La Liga/Bundesliga/Serie A
     - `add_star_players.py`: thêm cầu thủ sao cho Real/Barca/Atletico
     - `add_more_star_players.py`: thêm sao cho Bayern, AC Milan, Inter
     - `add_missing_players.py`: tự động tạo cầu thủ mẫu cho những đội chưa có cầu thủ

6. **Lỗi API key khi sync**
   - Đảm bảo đã đặt biến môi trường `FOOTBALL_DATA_API_KEY` (qua file `.env` như hướng dẫn ở trên)
   - Kiểm tra mạng và quota API; có thể cần tăng `API_DELAY` trong `services/football_api.py`

## ⚙️ Biến môi trường

- `FOOTBALL_DATA_API_KEY`: API key của football-data.org (yêu cầu cho sync)
- `FOOTBALL_DB` (tuỳ chọn): đường dẫn file SQLite DB. Mặc định là `footballinfor.db` cạnh `db.py`.

## 📝 Ghi chú phát triển

- **Framework:** Flask + Flask-Login
- **Database:** SQLite
- **Frontend:** Bootstrap 5 + Font Awesome
- **API:** football-data.org
- **Security:** Werkzeug password hashing
- **Development:** Debug mode enabled

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

---

**🎉 Chúc bạn sử dụng hệ thống hiệu quả!**
