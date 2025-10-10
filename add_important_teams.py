# add_important_teams.py - Thêm các teams quan trọng còn thiếu
import db

def add_important_teams():
    """Thêm các teams quan trọng còn thiếu"""
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    print("🔧 THÊM CÁC TEAMS QUAN TRỌNG CÒN THIẾU")
    print("=" * 50)
    
    # Lấy league IDs
    cur.execute("SELECT id, name FROM leagues WHERE name IN ('La Liga', 'Bundesliga', 'Serie A')")
    leagues = {row['name']: row['id'] for row in cur.fetchall()}
    
    # Thêm Real Madrid, Barcelona cho La Liga (nếu chưa có)
    la_liga_important = [
        {"name": "Real Madrid", "short_name": "RMA", "founded": 1902, "stadium": "Santiago Bernabéu", "external_id": 86},
        {"name": "Barcelona", "short_name": "BAR", "founded": 1899, "stadium": "Camp Nou", "external_id": 81},
        {"name": "Atletico Madrid", "short_name": "ATM", "founded": 1903, "stadium": "Wanda Metropolitano", "external_id": 78}
    ]
    
    # Thêm Bayern Munich, Dortmund cho Bundesliga
    bundesliga_important = [
        {"name": "Bayern Munich", "short_name": "FCB", "founded": 1900, "stadium": "Allianz Arena", "external_id": 5},
        {"name": "Borussia Dortmund", "short_name": "BVB", "founded": 1909, "stadium": "Signal Iduna Park", "external_id": 4},
        {"name": "Bayer Leverkusen", "short_name": "B04", "founded": 1904, "stadium": "BayArena", "external_id": 3},
        {"name": "VfB Stuttgart", "short_name": "VFB", "founded": 1893, "stadium": "Mercedes-Benz Arena", "external_id": 10},
        {"name": "Eintracht Frankfurt", "short_name": "SGE", "founded": 1899, "stadium": "Deutsche Bank Park", "external_id": 19}
    ]
    
    # Thêm AC Milan, Inter cho Serie A
    serie_a_important = [
        {"name": "AC Milan", "short_name": "MIL", "founded": 1899, "stadium": "San Siro", "external_id": 98},
        {"name": "Inter Milan", "short_name": "INT", "founded": 1908, "stadium": "San Siro", "external_id": 108},
        {"name": "Napoli", "short_name": "NAP", "founded": 1926, "stadium": "Diego Armando Maradona", "external_id": 113},
        {"name": "AS Roma", "short_name": "ROM", "founded": 1927, "stadium": "Stadio Olimpico", "external_id": 100},
        {"name": "Atalanta", "short_name": "ATA", "founded": 1907, "stadium": "Gewiss Stadium", "external_id": 102}
    ]
    
    # Thêm teams cho La Liga
    if 'La Liga' in leagues:
        for team in la_liga_important:
            cur.execute("""
                INSERT OR IGNORE INTO teams(league_id, name, short_name, founded_year, stadium, external_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (leagues['La Liga'], team['name'], team['short_name'], team['founded'], team['stadium'], team['external_id']))
        print("✅ Đã thêm teams quan trọng cho La Liga")
    
    # Thêm teams cho Bundesliga
    if 'Bundesliga' in leagues:
        for team in bundesliga_important:
            cur.execute("""
                INSERT OR IGNORE INTO teams(league_id, name, short_name, founded_year, stadium, external_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (leagues['Bundesliga'], team['name'], team['short_name'], team['founded'], team['stadium'], team['external_id']))
        print("✅ Đã thêm teams quan trọng cho Bundesliga")
    
    # Thêm teams cho Serie A
    if 'Serie A' in leagues:
        for team in serie_a_important:
            cur.execute("""
                INSERT OR IGNORE INTO teams(league_id, name, short_name, founded_year, stadium, external_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (leagues['Serie A'], team['name'], team['short_name'], team['founded'], team['stadium'], team['external_id']))
        print("✅ Đã thêm teams quan trọng cho Serie A")
    
    conn.commit()
    conn.close()
    print("🎉 Hoàn thành!")

if __name__ == "__main__":
    add_important_teams()

