# add_missing_players.py - Thêm cầu thủ mẫu cho các đội còn thiếu
import db
import random

def add_missing_players():
    """Thêm cầu thủ mẫu cho các đội chưa có cầu thủ"""
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    print("⚽ THÊM CẦU THỦ MẪU CHO CÁC ĐỘI CÒN THIẾU")
    print("=" * 60)
    
    # Lấy các đội chưa có cầu thủ
    cur.execute("""
        SELECT t.id, t.name, l.name as league_name
        FROM teams t
        LEFT JOIN leagues l ON l.id = t.league_id
        LEFT JOIN players p ON p.team_id = t.id
        WHERE p.id IS NULL
        ORDER BY l.name, t.name
    """)
    
    teams_without_players = cur.fetchall()
    print(f"📊 Tìm thấy {len(teams_without_players)} đội chưa có cầu thủ")
    print()
    
    # Danh sách tên cầu thủ mẫu
    first_names = [
        "Alex", "Bruno", "Carlos", "David", "Eduardo", "Fernando", "Gabriel", "Hugo",
        "Ivan", "João", "Kevin", "Lucas", "Miguel", "Nicolas", "Oscar", "Pedro",
        "Rafael", "Sergio", "Thiago", "Victor", "William", "Yuri", "Zé", "André",
        "Diego", "Felipe", "Gustavo", "Henrique", "Igor", "Julio", "Leonardo", "Marcos"
    ]
    
    last_names = [
        "Silva", "Santos", "Oliveira", "Costa", "Pereira", "Rodrigues", "Martins",
        "Ferreira", "Alves", "Lopes", "Gomes", "Ribeiro", "Carvalho", "Fernandes",
        "Gonçalves", "Dias", "Moreira", "Araújo", "Cunha", "Cardoso", "Reis",
        "Fonseca", "Correia", "Mendes", "Nunes", "Teixeira", "Torres", "Vieira"
    ]
    
    positions = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
    nationalities = [
        "Brazil", "Portugal", "Spain", "Argentina", "France", "Germany", "Italy",
        "England", "Netherlands", "Belgium", "Croatia", "Poland", "Colombia", "Uruguay"
    ]
    
    players_added = 0
    
    for team in teams_without_players:
        team_id = team[0]
        team_name = team[1]
        league_name = team[2]
        
        print(f"🏟️ {team_name} ({league_name})")
        
        # Tạo 20-30 cầu thủ mẫu cho mỗi đội
        num_players = random.randint(20, 30)
        
        for i in range(num_players):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            full_name = f"{first_name} {last_name}"
            position = random.choice(positions)
            nationality = random.choice(nationalities)
            shirt_number = random.randint(1, 99)
            
            # Tạo ngày sinh ngẫu nhiên (18-35 tuổi)
            birth_year = random.randint(1988, 2005)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            birthdate = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
            
            try:
                cur.execute("""
                    INSERT INTO players(
                        team_id, name, nationality, position, shirt_number, birthdate, external_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    team_id,
                    full_name,
                    nationality,
                    position,
                    shirt_number,
                    birthdate,
                    f"mock_{team_id}_{i+1}"
                ))
                players_added += 1
            except Exception as e:
                print(f"    ❌ Lỗi thêm cầu thủ {full_name}: {e}")
                continue
        
        print(f"  ✅ Đã thêm {num_players} cầu thủ mẫu")
        print()
    
    conn.commit()
    conn.close()
    
    print("=" * 60)
    print(f"📊 KẾT QUẢ:")
    print(f"  ✅ Đã thêm {players_added} cầu thủ mẫu")
    print(f"  🏟️ Cho {len(teams_without_players)} đội")
    print()
    print("🎉 Hoàn thành!")

if __name__ == "__main__":
    add_missing_players()

