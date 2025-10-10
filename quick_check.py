# quick_check.py - Kiểm tra nhanh hệ thống
import sqlite3
import os

def quick_check():
    """Kiểm tra nhanh hệ thống"""
    print("🔍 Kiểm tra nhanh Football Information System...")
    print("=" * 50)
    
    # Kiểm tra database
    db_path = "footballinfor.db"
    if os.path.exists(db_path):
        print("✅ Database tồn tại")
        
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            
            # Kiểm tra tables
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cur.fetchall()]
            print(f"✅ Tables: {', '.join(tables)}")
            
            # Kiểm tra dữ liệu
            for table in ['users', 'leagues', 'teams', 'players', 'matches']:
                if table in tables:
                    cur.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cur.fetchone()[0]
                    print(f"   📊 {table}: {count} records")
            
            # Kiểm tra admin user
            cur.execute("SELECT username, role FROM users WHERE role='admin'")
            admins = cur.fetchall()
            if admins:
                print(f"✅ Admin users: {[admin[0] for admin in admins]}")
            else:
                print("❌ Không có admin user")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Lỗi database: {e}")
    else:
        print("❌ Database không tồn tại")
    
    # Kiểm tra files quan trọng
    important_files = [
        'app.py', 'db.py', 'auth.py', 'decorators.py',
        'requirements.txt', 'create_admin.py', 'add_sample_data.py'
    ]
    
    print("\n📁 Kiểm tra files:")
    for file in important_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - THIẾU!")
    
    # Kiểm tra templates
    template_files = [
        'templates/base.html', 'templates/index.html', 'templates/dashboard.html',
        'templates/auth/login.html', 'templates/auth/register.html', 'templates/auth/profile.html'
    ]
    
    print("\n🎨 Kiểm tra templates:")
    for file in template_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - THIẾU!")
    
    print("\n" + "=" * 50)
    print("🎯 Hướng dẫn tiếp theo:")
    print("1. Chạy: python app.py")
    print("2. Mở: http://localhost:5000")
    print("3. Đăng nhập: admin / admin123")
    print("4. Test tất cả tính năng")

if __name__ == "__main__":
    quick_check()
