# sync_players.py - Lấy dữ liệu cầu thủ cho tất cả các đội
import os
import db
import requests
import time
from dotenv import load_dotenv

# API configuration from environment
load_dotenv()
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
BASE = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY} if API_KEY else None
API_DELAY = 6  # giây

def _get(url, params=None):
    """Helper function để gọi API với delay và kiểm tra API key"""
    if not HEADERS or not API_KEY:
        raise RuntimeError(
            "Missing FOOTBALL_DATA_API_KEY. Set it in your environment or .env file."
        )
    time.sleep(API_DELAY)
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()

def sync_players_for_all_teams():
    """Lấy dữ liệu cầu thủ cho tất cả các đội có external_id"""
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    print("⚽ LẤY DỮ LIỆU CẦU THỦ CHO TẤT CẢ CÁC ĐỘI")
    print("=" * 60)
    
    # Lấy tất cả teams có external_id
    cur.execute("""
        SELECT t.id, t.name, t.external_id, l.name as league_name
        FROM teams t
        LEFT JOIN leagues l ON l.id = t.league_id
        WHERE t.external_id IS NOT NULL
        ORDER BY l.name, t.name
    """)
    
    teams = cur.fetchall()
    print(f"📊 Tìm thấy {len(teams)} đội cần lấy dữ liệu cầu thủ")
    print()
    
    success_count = 0
    error_count = 0
    
    for i, team in enumerate(teams, 1):
        team_id = team['id']
        team_name = team['name']
        external_id = team['external_id']
        league_name = team['name']
        
        print(f"[{i}/{len(teams)}] 🏟️ {team_name} ({league_name})")
        
        try:
            # Kiểm tra xem đã có cầu thủ chưa
            cur.execute("SELECT COUNT(*) FROM players WHERE team_id = ?", (team_id,))
            existing_players = cur.fetchone()[0]
            
            if existing_players > 0:
                print(f"  ⏩ Đã có {existing_players} cầu thủ, bỏ qua...")
                continue
            
            # Lấy dữ liệu cầu thủ từ API
            team_detail = _get(f"{BASE}/teams/{external_id}")
            squad = team_detail.get("squad", [])
            
            if not squad:
                print(f"  ⚠️  Không có dữ liệu cầu thủ")
                continue
            
            # Thêm cầu thủ vào database
            players_added = 0
            for player in squad:
                try:
                    cur.execute("""
                        INSERT OR IGNORE INTO players(
                            team_id, name, nationality, position, shirt_number, birthdate, external_id
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        team_id,
                        player.get("name"),
                        player.get("nationality"),
                        player.get("position"),
                        player.get("shirtNumber"),
                        player.get("dateOfBirth"),
                        player.get("id")
                    ))
                    players_added += 1
                except Exception as e:
                    print(f"    ❌ Lỗi thêm cầu thủ {player.get('name', 'Unknown')}: {e}")
                    continue
            
            conn.commit()
            print(f"  ✅ Đã thêm {players_added} cầu thủ")
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ Lỗi: {e}")
            error_count += 1
            continue
        
        print()
    
    conn.close()
    
    print("=" * 60)
    print("📊 KẾT QUẢ:")
    print(f"  ✅ Thành công: {success_count} đội")
    print(f"  ❌ Lỗi: {error_count} đội")
    print(f"  📈 Tổng cộng: {len(teams)} đội")
    print()
    print("🎉 Hoàn thành!")

if __name__ == "__main__":
    sync_players_for_all_teams()

