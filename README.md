# ⚽ Football Information System

Hệ thống thông tin bóng đá toàn diện với chức năng đăng nhập phân quyền, quản lý dữ liệu từ các giải đấu hàng đầu thế giới.

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
├── 🔄 sync_players.py       # Sync dữ liệu cầu thủ (tùy chọn demo)
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

### Bước 4: Chạy ứng dụng (Docker khuyến nghị)

```bash
cp .env.example .env
# chỉnh sửa FLASK_SECRET_KEY
docker compose up -d --build
# mở http://localhost:5000
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
2. Click "Đăng nhập" ở góc phải
3. Nhập username và password
4. Click "Đăng nhập"

### 👑 Sử dụng với tài khoản Admin

1. Đăng nhập với `admin` / `admin123`
2. Dashboard: Click "Dashboard" để quản lý users
3. Quản lý Users:
   - Xem danh sách tất cả users
   - Thay đổi role (Admin ↔ User)
   - Xóa users (trừ chính mình)
4. Quản lý dữ liệu: Có thể thêm/sửa/xóa dữ liệu bóng đá

### 👤 Sử dụng với tài khoản User

1. Đăng nhập với `user` / `user123`
2. Xem dữ liệu: Chỉ có thể xem thông tin
3. Profile: Click tên user để xem profile
4. Giới hạn: Không thể truy cập Dashboard

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

- ✅ Password Hashing: Werkzeug
- ✅ Session Management: Flask-Login
- ✅ Role-based Access: Admin/User
- ✅ CSRF Protection
- ✅ Input Validation

## 🔄 Sync dữ liệu từ API (tùy chọn)

1) Đặt API key:
```bash
echo "FOOTBALL_DATA_API_KEY=your_api_key_here" >> .env
```
2) Chỉ sync cầu thủ cho các đội đã có external_id:
```bash
python sync_players.py
```

## ⚙️ Biến môi trường

- `FLASK_SECRET_KEY`: bắt buộc (sản xuất)
- `FOOTBALL_DATA_API_KEY`: tuỳ chọn, phục vụ đồng bộ dữ liệu
- `FOOTBALL_DB`: tuỳ chọn, đường dẫn SQLite (Docker default `/data/footballinfor.db`)

## 📝 Ghi chú phát triển

- Framework: Flask + Flask-Login
- Database: SQLite
- Frontend: Bootstrap 5 + Font Awesome
- Security: Werkzeug password hashing
- Development: Debug mode enabled

---
**🎉 Chúc bạn sử dụng hệ thống hiệu quả!**
