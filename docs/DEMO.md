## Hướng dẫn Demo Nhanh

### 1) Chuẩn bị
- Cần Docker và Docker Compose.
- Tùy chọn: copy `.env.example` thành `.env` và chỉnh các biến theo nhu cầu.

### 2) Chạy ứng dụng bằng Docker (Gunicorn)
```bash
docker compose up -d --build
# Đợi container healthy rồi mở:
http://localhost:5000
```
- Tài khoản mặc định (nếu bật `CREATE_DEFAULT_USERS=1`):
  - Admin: `admin / admin123`
- Dữ liệu lưu tại volume `app-data` (mặc định mount `/data` trong container). SQLite file nằm ở `/data/footballinfor.db`.

### 3) Thêm dữ liệu mẫu (tùy chọn)
```bash
docker compose exec web python -c "import db; db.init_db()"
docker compose exec web python add_sample_data.py
```

### 4) Kiểm tra nhanh (health + smoke test)
```bash
# Health check thủ công (trả 200)
curl -sSf http://localhost:5000 >/dev/null && echo OK || echo FAIL

# Test tích hợp thủ công (yêu cầu service đang chạy localhost:5000)
docker compose exec web python test_system.py
```

### 5) Quét bảo mật local (tùy chọn)
```bash
bash scripts/scan.sh
# hoặc
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
make scan-all
```

### 6) Deploy miễn phí lên Render (1-click)
- Repo đã có `render.yaml` (Blueprint) để 1-click deploy.
- Các bước:
  1. Push repo lên GitHub.
  2. Vào Render → New → Blueprint → chọn repo.
  3. Render tự build Dockerfile, chạy Gunicorn. Mặc định gắn disk 1GB tại `/app/data`.
  4. Xác nhận/env:
     - `FLASK_SECRET_KEY` (auto-generate)
     - `CREATE_DEFAULT_USERS=1`
     - `FOOTBALL_DATA_API_KEY` (nếu dùng)
     - `PORT=5000`
     - `GUNICORN_WORKERS=1`
  5. Deploy và mở URL.

### 7) Gỡ lỗi thường gặp
- 502/Starting up lâu: chờ build xong, kiểm tra Logs.
- DB lỗi quyền: đảm bảo disk đã gắn vào `/app/data` (Render) hoặc volume `app-data` (Compose).
- SECRET_KEY trống: đặt biến `FLASK_SECRET_KEY` trong `.env` hoặc Render env.
