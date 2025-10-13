================================================================================
                    🚀 HƯỚNG DẪN CHẠY DEMO NHANH
================================================================================

📁 Dự án: Football Information System - DevSecOps
📅 Cập nhật: 2025-10-13

================================================================================
                    ⚡ DEMO NHANH (1 LỆNH - 5 PHÚT)
================================================================================

Chạy script tự động:

    .\demo-all.ps1

Script sẽ tự động:
  ✅ Kiểm tra hệ thống
  ✅ Build Docker image
  ✅ Start container
  ✅ Test application
  ✅ Chạy security scans
  ✅ Tạo reports
  ✅ Mở browser

================================================================================
                    📋 DEMO THỦ CÔNG (TỪNG BƯỚC)
================================================================================

Xem file: LENH_DEMO.txt

Hoặc làm theo các bước sau:

BƯỚC 1: Start Docker
---------------------
docker-compose up -d

BƯỚC 2: Kiểm tra
-----------------
docker-compose ps
curl http://localhost:5000

BƯỚC 3: Security Scans
-----------------------
.\security-scan.ps1

BƯỚC 4: Xem Reports
--------------------
Get-ChildItem reports\
type reports\bandit-report.txt
type reports\safety-report.txt
type reports\trivy-report.txt

BƯỚC 5: Stop
------------
docker-compose down

================================================================================
                    📚 TÀI LIỆU CHI TIẾT
================================================================================

1. HUONG_DAN_DEVSECOPS.md
   → Hướng dẫn đầy đủ từ A-Z

2. LENH_DEMO.txt
   → Tất cả lệnh demo chi tiết

3. README.md
   → Giới thiệu dự án

4. SETUP_SUMMARY.txt
   → Tóm tắt setup

================================================================================
                    🎯 DEMO FLOW KHUYẾN NGHỊ
================================================================================

Thời gian: 15 phút

Phút 1-2:   Giới thiệu DevSecOps
Phút 3-5:   Demo Docker (.\demo-all.ps1)
Phút 6-8:   Show security reports
Phút 9-10:  Demo GitHub Actions
Phút 11-14: Demo cloud deployment
Phút 15:    Q&A

================================================================================
                    ✅ CHECKLIST TRƯỚC KHI DEMO
================================================================================

□ Docker Desktop đang chạy
□ Đã cài đặt: Python, Git, Docker, Bandit, Safety, Trivy
□ Đã clone project
□ Đã activate virtual environment
□ Đã install dependencies
□ File .env đã configure

================================================================================
                    🆘 TROUBLESHOOTING
================================================================================

Lỗi: Container không chạy
→ docker logs football-app
→ docker-compose down
→ docker-compose build --no-cache
→ docker-compose up -d

Lỗi: Port 5000 bị chiếm
→ netstat -ano | findstr :5000
→ taskkill /PID <PID> /F

Lỗi: Trivy not found
→ choco install trivy -y (PowerShell as Admin)

================================================================================
                    📞 LIÊN HỆ
================================================================================

GitHub: https://github.com/thangnt04-scr/FB-News
Documentation: HUONG_DAN_DEVSECOPS.md

================================================================================

