# add_star_players.py - Thêm cầu thủ sao cho các đội lớn
import db
import random

def add_star_players():
    """Thêm cầu thủ sao cho Real Madrid, Barcelona và các đội lớn"""
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    print("⭐ THÊM CẦU THỦ SAO CHO CÁC ĐỘI LỚN")
    print("=" * 60)
    
    # Lấy các đội lớn trong La Liga
    cur.execute("""
        SELECT t.id, t.name, l.name as league_name
        FROM teams t
        LEFT JOIN leagues l ON l.id = t.league_id
        WHERE l.name = 'La Liga' AND t.name IN ('Real Madrid', 'Barcelona', 'Atletico Madrid')
        ORDER BY t.name
    """)
    
    big_teams = cur.fetchall()
    
    # Danh sách cầu thủ sao thực tế
    real_madrid_players = [
        {"name": "Vinicius Jr.", "position": "Left Winger", "nationality": "Brazil", "shirt_number": 7, "birthdate": "2000-07-12"},
        {"name": "Jude Bellingham", "position": "Attacking Midfield", "nationality": "England", "shirt_number": 5, "birthdate": "2003-06-29"},
        {"name": "Kylian Mbappé", "position": "Centre-Forward", "nationality": "France", "shirt_number": 9, "birthdate": "1998-12-20"},
        {"name": "Luka Modrić", "position": "Central Midfield", "nationality": "Croatia", "shirt_number": 10, "birthdate": "1985-09-09"},
        {"name": "Toni Kroos", "position": "Central Midfield", "nationality": "Germany", "shirt_number": 8, "birthdate": "1990-01-04"},
        {"name": "Thibaut Courtois", "position": "Goalkeeper", "nationality": "Belgium", "shirt_number": 1, "birthdate": "1992-05-11"},
        {"name": "David Alaba", "position": "Centre-Back", "nationality": "Austria", "shirt_number": 4, "birthdate": "1992-06-24"},
        {"name": "Éder Militão", "position": "Centre-Back", "nationality": "Brazil", "shirt_number": 3, "birthdate": "1998-01-18"},
        {"name": "Ferland Mendy", "position": "Left-Back", "nationality": "France", "shirt_number": 23, "birthdate": "1995-06-08"},
        {"name": "Dani Carvajal", "position": "Right-Back", "nationality": "Spain", "shirt_number": 2, "birthdate": "1992-01-11"},
        {"name": "Federico Valverde", "position": "Central Midfield", "nationality": "Uruguay", "shirt_number": 15, "birthdate": "1998-07-22"},
        {"name": "Rodrygo", "position": "Right Winger", "nationality": "Brazil", "shirt_number": 11, "birthdate": "2001-01-09"},
        {"name": "Eduardo Camavinga", "position": "Defensive Midfield", "nationality": "France", "shirt_number": 12, "birthdate": "2002-11-10"},
        {"name": "Aurélien Tchouaméni", "position": "Defensive Midfield", "nationality": "France", "shirt_number": 18, "birthdate": "2000-01-27"},
        {"name": "Joselu", "position": "Centre-Forward", "nationality": "Spain", "shirt_number": 14, "birthdate": "1990-03-27"},
        {"name": "Lucas Vázquez", "position": "Right Winger", "nationality": "Spain", "shirt_number": 17, "birthdate": "1991-07-01"},
        {"name": "Nacho", "position": "Centre-Back", "nationality": "Spain", "shirt_number": 6, "birthdate": "1990-01-18"},
        {"name": "Fran García", "position": "Left-Back", "nationality": "Spain", "shirt_number": 20, "birthdate": "1999-08-14"},
        {"name": "Kepa Arrizabalaga", "position": "Goalkeeper", "nationality": "Spain", "shirt_number": 25, "birthdate": "1994-10-03"},
        {"name": "Brahim Díaz", "position": "Attacking Midfield", "nationality": "Spain", "shirt_number": 21, "birthdate": "1999-08-03"}
    ]
    
    barcelona_players = [
        {"name": "Robert Lewandowski", "position": "Centre-Forward", "nationality": "Poland", "shirt_number": 9, "birthdate": "1988-08-21"},
        {"name": "Pedri", "position": "Central Midfield", "nationality": "Spain", "shirt_number": 8, "birthdate": "2002-11-25"},
        {"name": "Gavi", "position": "Central Midfield", "nationality": "Spain", "shirt_number": 6, "birthdate": "2004-08-05"},
        {"name": "Frenkie de Jong", "position": "Central Midfield", "nationality": "Netherlands", "shirt_number": 21, "birthdate": "1997-05-12"},
        {"name": "Marc-André ter Stegen", "position": "Goalkeeper", "nationality": "Germany", "shirt_number": 1, "birthdate": "1992-04-30"},
        {"name": "Ronald Araújo", "position": "Centre-Back", "nationality": "Uruguay", "shirt_number": 4, "birthdate": "1999-03-07"},
        {"name": "Jules Koundé", "position": "Centre-Back", "nationality": "France", "shirt_number": 23, "birthdate": "1998-11-12"},
        {"name": "Alejandro Balde", "position": "Left-Back", "nationality": "Spain", "shirt_number": 3, "birthdate": "2003-10-18"},
        {"name": "João Cancelo", "position": "Right-Back", "nationality": "Portugal", "shirt_number": 2, "birthdate": "1994-05-27"},
        {"name": "Raphinha", "position": "Right Winger", "nationality": "Brazil", "shirt_number": 11, "birthdate": "1996-12-14"},
        {"name": "Ousmane Dembélé", "position": "Right Winger", "nationality": "France", "shirt_number": 7, "birthdate": "1997-05-15"},
        {"name": "Ferran Torres", "position": "Left Winger", "nationality": "Spain", "shirt_number": 7, "birthdate": "2000-02-29"},
        {"name": "Ansu Fati", "position": "Left Winger", "nationality": "Spain", "shirt_number": 10, "birthdate": "2002-10-31"},
        {"name": "Sergio Busquets", "position": "Defensive Midfield", "nationality": "Spain", "shirt_number": 5, "birthdate": "1988-07-16"},
        {"name": "Ilkay Gündoğan", "position": "Central Midfield", "nationality": "Germany", "shirt_number": 22, "birthdate": "1990-10-24"},
        {"name": "Andreas Christensen", "position": "Centre-Back", "nationality": "Denmark", "shirt_number": 15, "birthdate": "1996-04-10"},
        {"name": "Marcos Alonso", "position": "Left-Back", "nationality": "Spain", "shirt_number": 17, "birthdate": "1990-12-28"},
        {"name": "Sergi Roberto", "position": "Right-Back", "nationality": "Spain", "shirt_number": 20, "birthdate": "1992-02-07"},
        {"name": "Inaki Peña", "position": "Goalkeeper", "nationality": "Spain", "shirt_number": 13, "birthdate": "1999-03-02"}
    ]
    
    atletico_players = [
        {"name": "Antoine Griezmann", "position": "Centre-Forward", "nationality": "France", "shirt_number": 7, "birthdate": "1991-03-21"},
        {"name": "Álvaro Morata", "position": "Centre-Forward", "nationality": "Spain", "shirt_number": 19, "birthdate": "1992-10-23"},
        {"name": "Koke", "position": "Central Midfield", "nationality": "Spain", "shirt_number": 6, "birthdate": "1992-01-08"},
        {"name": "Jan Oblak", "position": "Goalkeeper", "nationality": "Slovenia", "shirt_number": 13, "birthdate": "1993-01-07"},
        {"name": "José Giménez", "position": "Centre-Back", "nationality": "Uruguay", "shirt_number": 2, "birthdate": "1995-01-20"},
        {"name": "Stefan Savić", "position": "Centre-Back", "nationality": "Montenegro", "shirt_number": 15, "birthdate": "1991-01-08"},
        {"name": "Reinildo", "position": "Left-Back", "nationality": "Mozambique", "shirt_number": 23, "birthdate": "1994-01-21"},
        {"name": "Nahuel Molina", "position": "Right-Back", "nationality": "Argentina", "shirt_number": 16, "birthdate": "1998-04-06"},
        {"name": "Rodrigo de Paul", "position": "Central Midfield", "nationality": "Argentina", "shirt_number": 5, "birthdate": "1994-05-24"},
        {"name": "Marcos Llorente", "position": "Right Midfield", "nationality": "Spain", "shirt_number": 14, "birthdate": "1995-01-30"},
        {"name": "Saúl Ñíguez", "position": "Central Midfield", "nationality": "Spain", "shirt_number": 8, "birthdate": "1994-11-21"},
        {"name": "Thomas Lemar", "position": "Left Winger", "nationality": "France", "shirt_number": 11, "birthdate": "1995-11-12"},
        {"name": "Yannick Carrasco", "position": "Left Winger", "nationality": "Belgium", "shirt_number": 21, "birthdate": "1993-09-04"},
        {"name": "Ángel Correa", "position": "Right Winger", "nationality": "Argentina", "shirt_number": 10, "birthdate": "1995-03-09"},
        {"name": "Matheus Cunha", "position": "Centre-Forward", "nationality": "Brazil", "shirt_number": 9, "birthdate": "1999-05-27"},
        {"name": "Mario Hermoso", "position": "Centre-Back", "nationality": "Spain", "shirt_number": 4, "birthdate": "1995-06-18"},
        {"name": "Kieran Trippier", "position": "Right-Back", "nationality": "England", "shirt_number": 23, "birthdate": "1990-09-19"},
        {"name": "Felipe", "position": "Centre-Back", "nationality": "Brazil", "shirt_number": 18, "birthdate": "1989-05-16"},
        {"name": "Ivo Grbić", "position": "Goalkeeper", "nationality": "Croatia", "shirt_number": 1, "birthdate": "1996-01-18"},
        {"name": "Antonio Rüdiger", "position": "Centre-Back", "nationality": "Germany", "shirt_number": 22, "birthdate": "1993-03-03"}
    ]
    
    # Thêm cầu thủ cho Real Madrid
    real_madrid_team = next((t for t in big_teams if 'Real Madrid' in t[1]), None)
    if real_madrid_team:
        print(f"\n⚽ Thêm cầu thủ cho Real Madrid...")
        for player in real_madrid_players:
            cur.execute("""
                INSERT OR IGNORE INTO players(
                    team_id, name, nationality, position, shirt_number, birthdate, external_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                real_madrid_team[0],
                player['name'],
                player['nationality'],
                player['position'],
                player['shirt_number'],
                player['birthdate'],
                f"real_{player['name'].replace(' ', '_').lower()}"
            ))
        print(f"  ✅ Đã thêm {len(real_madrid_players)} cầu thủ cho Real Madrid")
    
    # Thêm cầu thủ cho Barcelona
    barcelona_team = next((t for t in big_teams if 'Barcelona' in t[1]), None)
    if barcelona_team:
        print(f"\n⚽ Thêm cầu thủ cho Barcelona...")
        for player in barcelona_players:
            cur.execute("""
                INSERT OR IGNORE INTO players(
                    team_id, name, nationality, position, shirt_number, birthdate, external_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                barcelona_team[0],
                player['name'],
                player['nationality'],
                player['position'],
                player['shirt_number'],
                player['birthdate'],
                f"barca_{player['name'].replace(' ', '_').lower()}"
            ))
        print(f"  ✅ Đã thêm {len(barcelona_players)} cầu thủ cho Barcelona")
    
    # Thêm cầu thủ cho Atletico Madrid
    atletico_team = next((t for t in big_teams if 'Atletico Madrid' in t[1]), None)
    if atletico_team:
        print(f"\n⚽ Thêm cầu thủ cho Atletico Madrid...")
        for player in atletico_players:
            cur.execute("""
                INSERT OR IGNORE INTO players(
                    team_id, name, nationality, position, shirt_number, birthdate, external_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                atletico_team[0],
                player['name'],
                player['nationality'],
                player['position'],
                player['shirt_number'],
                player['birthdate'],
                f"atletico_{player['name'].replace(' ', '_').lower()}"
            ))
        print(f"  ✅ Đã thêm {len(atletico_players)} cầu thủ cho Atletico Madrid")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Hoàn thành! Đã thêm cầu thủ sao cho các đội lớn La Liga")

if __name__ == "__main__":
    add_star_players()

