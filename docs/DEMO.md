# Demo triển khai DevSecOps + Render

## I. Chuẩn bị môi trường
- Cần Docker và Docker Compose, hoặc Python 3.12
- Sao chép biến môi trường mẫu:
```bash
cp .env.example .env
# chỉnh sửa FLASK_SECRET_KEY
```

## II. Docker hóa ứng dụng
- Đã có `Dockerfile`, `.dockerignore`, `docker-compose.yml`, `scripts/entrypoint.sh`
- Chạy local:
```bash
docker compose up -d --build
# mở http://localhost:5000
```

## III. Quét bảo mật thủ công (Local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
make scan-all
# hoặcash scripts/scan.sh
```

## IV. Tích hợp tự động (CI/CD)
- Workflow: `.github/workflows/devsecops.yml`
- Pipeline: lint → test → bandit → pip-audit → build/push GHCR → Trivy

## V. Triển khai lên Cloud (Render)
- File `render.yaml` đã cấu hình service `web` (plan free) dùng Docker
- Các bước:
  1. Kết nối repo GitHub tới Render, chọn auto deploy
  2. Cấu hình env vars: `FLASK_SECRET_KEY` (bắt buộc), `FOOTBALL_DATA_API_KEY` (tùy chọn)
  3. Add persistent disk `/data` (Render dùng `disk:` trong render.yaml)
  4. Deploy và theo dõi logs

## VI. Báo cáo & Minh chứng
- Tài liệu: `docs/DevSecOps-Report.md`, `docs/DEMO.md`
- Artifacts CI: `bandit.txt`, `pip-audit.json`, `trivy-image.sarif` trên GitHub Actions

## Tài khoản mặc định
- Admin: `admin` / `admin123`
- User: `user` / `user123`
