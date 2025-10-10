# create_admin.py - Script tạo admin user mặc định
import db
import auth

def create_default_admin():
    """Tạo admin user mặc định"""
    admin_username = "admin"
    admin_email = "admin@football.com"
    admin_password = "admin123"
    
    # Kiểm tra xem admin đã tồn tại chưa
    existing_admin = db.get_user_by_username(admin_username)
    if existing_admin:
        print(f"Admin user '{admin_username}' đã tồn tại!")
        return False
    
    # Tạo admin user
    if auth.User.create_user(admin_username, admin_email, admin_password, 'admin'):
        print(f"✅ Tạo admin user thành công!")
        print(f"   Username: {admin_username}")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        print(f"   Role: admin")
        return True
    else:
        print("❌ Không thể tạo admin user!")
        return False

def create_test_user():
    """Tạo test user"""
    test_username = "user"
    test_email = "user@football.com"
    test_password = "user123"
    
    # Kiểm tra xem user đã tồn tại chưa
    existing_user = db.get_user_by_username(test_username)
    if existing_user:
        print(f"Test user '{test_username}' đã tồn tại!")
        return False
    
    # Tạo test user
    if auth.User.create_user(test_username, test_email, test_password, 'user'):
        print(f"✅ Tạo test user thành công!")
        print(f"   Username: {test_username}")
        print(f"   Email: {test_email}")
        print(f"   Password: {test_password}")
        print(f"   Role: user")
        return True
    else:
        print("❌ Không thể tạo test user!")
        return False

if __name__ == "__main__":
    print("🚀 Tạo users mặc định...")
    print("=" * 50)
    
    # Khởi tạo database
    db.init_db()
    
    # Tạo admin
    create_default_admin()
    print()
    
    # Tạo test user
    create_test_user()
    print()
    
    print("=" * 50)
    print("✅ Hoàn thành! Bạn có thể đăng nhập với:")
    print("   Admin: admin / admin123")
    print("   User:  user / user123")
