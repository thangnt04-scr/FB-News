## DevSecOps Pipeline - Báo cáo và minh chứng

### 1) Chuẩn bị môi trường
- Chuẩn hóa `SECRET_KEY` đọc từ biến môi trường.
- Thêm `.env.example` để cấu hình nhanh.

### 2) Docker hóa ứng dụng
- Tạo `Dockerfile`, `.dockerignore`, `docker-compose.yml`.
- `ENTRYPOINT` khởi tạo DB, tạo user mẫu khi cần.

### 3) Quét bảo mật thủ công (local)
- `requirements-dev.txt` gồm: flake8, black, pytest, bandit, pip-audit, safety.
- Script: `scripts/scan.sh` hoặc dùng `make scan-all`.
- Bằng chứng: output artifacts khi chạy cục bộ (nên commit artifact vào CI thay vì repo).

### 4) Tích hợp tự động (CI/CD)
- Workflow `devsecops.yml`: Lint, Test, SAST (bandit), Dependency scan (pip-audit), Build & push image lên GHCR.
- Artifacts: `bandit.txt`, `pip-audit.json` được upload.

### 5) Triển khai lên Cloud
- Workflow `deploy-azure.yml`: deploy image từ GHCR lên Azure Web App (Container).
- Secrets cần có:
  - `AZURE_CREDENTIALS` (JSON service principal)
  - `AZURE_WEBAPP_NAME`
  - `FLASK_SECRET_KEY`
  - `FOOTBALL_DATA_API_KEY`

### 6) Cách reproduce local
```bash
# Build & run
docker compose up -d --build

# Mở http://localhost:5000
# Admin mặc định: admin / admin123 (có thể vô hiệu bằng CREATE_DEFAULT_USERS=0)

# Quét bảo mật local
bash scripts/scan.sh
# hoặc
make install-dev
make scan-all
```
