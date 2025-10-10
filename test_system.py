# test_system.py - Script test hệ thống
import requests
import json

def test_system():
    """Test tất cả các tính năng của hệ thống"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Football Information System...")
    print("=" * 50)
    
    # Test 1: Trang chủ
    print("1. Testing trang chủ...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("   ✅ Trang chủ hoạt động")
        else:
            print(f"   ❌ Trang chủ lỗi: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Không thể kết nối: {e}")
        return
    
    # Test 2: API Leagues
    print("2. Testing API leagues...")
    try:
        response = requests.get(f"{base_url}/api/leagues")
        if response.status_code == 200:
            leagues = response.json()
            print(f"   ✅ API leagues hoạt động - {len(leagues)} leagues")
        else:
            print(f"   ❌ API leagues lỗi: {response.status_code}")
    except Exception as e:
        print(f"   ❌ API leagues lỗi: {e}")
    
    # Test 3: API Search
    print("3. Testing API search...")
    try:
        response = requests.get(f"{base_url}/api/search?q=Manchester")
        if response.status_code == 200:
            results = response.json()
            print(f"   ✅ API search hoạt động - {len(results)} kết quả")
            for result in results[:3]:  # Hiển thị 3 kết quả đầu
                print(f"      - {result['name']} ({result['type']})")
        else:
            print(f"   ❌ API search lỗi: {response.status_code}")
    except Exception as e:
        print(f"   ❌ API search lỗi: {e}")
    
    # Test 4: Login
    print("4. Testing login...")
    try:
        session = requests.Session()
        # Lấy trang login
        response = session.get(f"{base_url}/login")
        if response.status_code == 200:
            # Thử đăng nhập
            login_data = {
                'username': 'admin',
                'password': 'admin123'
            }
            response = session.post(f"{base_url}/login", data=login_data)
            if response.status_code == 302:  # Redirect sau khi login thành công
                print("   ✅ Login admin thành công")
                
                # Test dashboard
                response = session.get(f"{base_url}/dashboard")
                if response.status_code == 200:
                    print("   ✅ Dashboard admin hoạt động")
                else:
                    print(f"   ❌ Dashboard lỗi: {response.status_code}")
            else:
                print(f"   ❌ Login thất bại: {response.status_code}")
        else:
            print(f"   ❌ Trang login lỗi: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Login test lỗi: {e}")
    
    # Test 5: Team page
    print("5. Testing team page...")
    try:
        response = requests.get(f"{base_url}/team/1")
        if response.status_code == 200:
            print("   ✅ Team page hoạt động")
        else:
            print(f"   ❌ Team page lỗi: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Team page lỗi: {e}")
    
    # Test 6: League page
    print("6. Testing league page...")
    try:
        response = requests.get(f"{base_url}/league/1")
        if response.status_code == 200:
            print("   ✅ League page hoạt động")
        else:
            print(f"   ❌ League page lỗi: {response.status_code}")
    except Exception as e:
        print(f"   ❌ League page lỗi: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Test hoàn thành!")
    print("\n📋 Hướng dẫn test thủ công:")
    print("1. Mở trình duyệt: http://localhost:5000")
    print("2. Đăng nhập admin: admin / admin123")
    print("3. Test Dashboard, quản lý users")
    print("4. Test tìm kiếm: gõ 'Manchester', 'Messi', 'Real'")
    print("5. Click vào leagues, teams, players")
    print("6. Test responsive design")

if __name__ == "__main__":
    test_system()

