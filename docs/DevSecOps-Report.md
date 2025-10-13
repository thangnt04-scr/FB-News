# DevSecOps Implementation Report

## I. Chuẩn bị môi trường
- Python 3.12
- Virtualenv hoặc Docker
- Biến môi trường: `FLASK_SECRET_KEY`, `FOOTBALL_DB` (tùy chọn), `FOOTBALL_DATA_API_KEY` (tùy chọn)

## II. Docker hóa ứng dụng
- Dockerfile multi-stage nhẹ (python:3.12-slim)
- Entrypoint khởi tạo DB và tạo user demo
- docker-compose với volume `/data`

## III. Quét bảo mật thủ công (local)
```bash
bash scripts/scan.sh
```
- flake8, pytest (bỏ `test_system`), bandit, pip-audit

## IV. Tích hợp tự động (CI/CD DevSecOps)
- Workflow: `.github/workflows/devsecops.yml`
- Jobs: Lint, Test, SAST (Bandit), Dependency Scan (pip-audit), Build & Push GHCR, Trivy Image
- Artifacts: `bandit.txt`, `pip-audit.json`, `trivy-image.sarif`

## V. Triển khai lên Cloud (Render)
- File: `render.yaml`
- Plan: free
- Persistent disk `/data` để lưu SQLite DB
- Env cần thiết: `FLASK_SECRET_KEY` (bắt buộc), `FOOTBALL_DATA_API_KEY` (nếu dùng sync)
- Deploy bằng cách kết nối repo với Render, auto deploy khi push

## VI. Báo cáo và minh chứng
- Tài liệu này + artifacts CI
- Hướng dẫn demo kèm dưới đây

---

## Hướng dẫn Demo Nhanh

### 1) Chạy local bằng Docker
```bash
cp .env.example .env
# Sửa FLASK_SECRET_KEY cho an toàn
docker compose up -d --build
open http://localhost:5000
```
Mặc định tạo admin `admin/admin123` và user `user/user123`.

### 2) Quét bảo mật local
```bash
bash scripts/scan.sh
```

### 3) CI/CD trên GitHub
- Mở tab Actions, xem workflow DevSecOps CI
- Artifacts: security-reports (bandit/pip-audit), trivy-image.sarif
- Image được push lên `ghcr.io/<owner>/<repo>:<tags>`

### 4) Deploy Render
- Tạo dịch vụ Web trên Render, chọn "Deploy from repo" và cung cấp `render.yaml`
- Set env vars: `FLASK_SECRET_KEY`, `FOOTBALL_DATA_API_KEY` (nếu cần)
- Kiểm tra Logs, truy cập endpoint public của Render

### 5) Đồng bộ dữ liệu (tùy chọn)
- Đặt `FOOTBALL_DATA_API_KEY`
- Chạy `sync_all.py` bằng Render shell hoặc tạm thời bật job riêng
