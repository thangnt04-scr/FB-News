# add_more_star_players.py - Thêm cầu thủ sao cho các đội lớn khác
import db

def add_more_star_players():
    """Thêm cầu thủ sao cho các đội lớn khác"""
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    print("⭐ THÊM CẦU THỦ SAO CHO CÁC ĐỘI LỚN KHÁC")
    print("=" * 60)
    
    # Bayern Munich players
    bayern_players = [
        {"name": "Harry Kane", "position": "Centre-Forward", "nationality": "England", "shirt_number": 9, "birthdate": "1993-07-28"},
        {"name": "Leroy Sané", "position": "Right Winger", "nationality": "Germany", "shirt_number": 10, "birthdate": "1996-01-11"},
        {"name": "Kingsley Coman", "position": "Left Winger", "nationality": "France", "shirt_number": 11, "birthdate": "1996-06-13"},
        {"name": "Thomas Müller", "position": "Attacking Midfield", "nationality": "Germany", "shirt_number": 25, "birthdate": "1989-09-13"},
        {"name": "Joshua Kimmich", "position": "Defensive Midfield", "nationality": "Germany", "shirt_number": 6, "birthdate": "1995-02-08"},
        {"name": "Leon Goretzka", "position": "Central Midfield", "nationality": "Germany", "shirt_number": 8, "birthdate": "1995-02-06"},
        {"name": "Manuel Neuer", "position": "Goalkeeper", "nationality": "Germany", "shirt_number": 1, "birthdate": "1986-03-27"},
        {"name": "Matthijs de Ligt", "position": "Centre-Back", "nationality": "Netherlands", "shirt_number": 4, "birthdate": "1999-08-12"},
        {"name": "Dayot Upamecano", "position": "Centre-Back", "nationality": "France", "shirt_number": 2, "birthdate": "1998-10-27"},
        {"name": "Alphonso Davies", "position": "Left-Back", "nationality": "Canada", "shirt_number": 19, "birthdate": "2000-11-02"},
        {"name": "Benjamin Pavard", "position": "Right-Back", "nationality": "France", "shirt_number": 5, "birthdate": "1996-03-28"},
        {"name": "Serge Gnabry", "position": "Right Winger", "nationality": "Germany", "shirt_number": 7, "birthdate": "1995-07-14"},
        {"name": "Jamal Musiala", "position": "Attacking Midfield", "nationality": "Germany", "shirt_number": 42, "birthdate": "2003-02-26"},
        {"name": "Eric Maxim Choupo-Moting", "position": "Centre-Forward", "nationality": "Cameroon", "shirt_number": 13, "birthdate": "1989-03-23"},
        {"name": "Ryan Gravenberch", "position": "Central Midfield", "nationality": "Netherlands", "shirt_number": 38, "birthdate": "2002-05-16"}
    ]
    
    # AC Milan players
    ac_milan_players = [
        {"name": "Olivier Giroud", "position": "Centre-Forward", "nationality": "France", "shirt_number": 9, "birthdate": "1986-09-30"},
        {"name": "Rafael Leão", "position": "Left Winger", "nationality": "Portugal", "shirt_number": 17, "birthdate": "1999-06-10"},
        {"name": "Theo Hernández", "position": "Left-Back", "nationality": "France", "shirt_number": 19, "birthdate": "1997-10-06"},
        {"name": "Ismaël Bennacer", "position": "Defensive Midfield", "nationality": "Algeria", "shirt_number": 4, "birthdate": "1997-12-01"},
        {"name": "Sandro Tonali", "position": "Central Midfield", "nationality": "Italy", "shirt_number": 8, "birthdate": "2000-05-08"},
        {"name": "Mike Maignan", "position": "Goalkeeper", "nationality": "France", "shirt_number": 16, "birthdate": "1995-07-03"},
        {"name": "Fikayo Tomori", "position": "Centre-Back", "nationality": "England", "shirt_number": 23, "birthdate": "1997-12-19"},
        {"name": "Alessio Romagnoli", "position": "Centre-Back", "nationality": "Italy", "shirt_number": 13, "birthdate": "1995-01-12"},
        {"name": "Davide Calabria", "position": "Right-Back", "nationality": "Italy", "shirt_number": 2, "birthdate": "1996-12-06"},
        {"name": "Brahim Díaz", "position": "Attacking Midfield", "nationality": "Spain", "shirt_number": 10, "birthdate": "1999-08-03"},
        {"name": "Ante Rebić", "position": "Left Winger", "nationality": "Croatia", "shirt_number": 12, "birthdate": "1993-09-21"},
        {"name": "Franck Kessié", "position": "Central Midfield", "nationality": "Ivory Coast", "shirt_number": 79, "birthdate": "1996-12-19"},
        {"name": "Zlatan Ibrahimović", "position": "Centre-Forward", "nationality": "Sweden", "shirt_number": 11, "birthdate": "1981-10-03"},
        {"name": "Simon Kjær", "position": "Centre-Back", "nationality": "Denmark", "shirt_number": 24, "birthdate": "1989-03-26"},
        {"name": "Hakan Çalhanoğlu", "position": "Attacking Midfield", "nationality": "Turkey", "shirt_number": 10, "birthdate": "1994-02-08"}
    ]
    
    # Inter Milan players
    inter_milan_players = [
        {"name": "Lautaro Martínez", "position": "Centre-Forward", "nationality": "Argentina", "shirt_number": 10, "birthdate": "1997-08-22"},
        {"name": "Romelu Lukaku", "position": "Centre-Forward", "nationality": "Belgium", "shirt_number": 90, "birthdate": "1993-05-13"},
        {"name": "Nicolò Barella", "position": "Central Midfield", "nationality": "Italy", "shirt_number": 23, "birthdate": "1997-02-07"},
        {"name": "Marcelo Brozović", "position": "Defensive Midfield", "nationality": "Croatia", "shirt_number": 77, "birthdate": "1992-11-16"},
        {"name": "Samir Handanović", "position": "Goalkeeper", "nationality": "Slovenia", "shirt_number": 1, "birthdate": "1984-07-14"},
        {"name": "Milan Škriniar", "position": "Centre-Back", "nationality": "Slovakia", "shirt_number": 37, "birthdate": "1995-02-11"},
        {"name": "Alessandro Bastoni", "position": "Centre-Back", "nationality": "Italy", "shirt_number": 95, "birthdate": "1999-04-13"},
        {"name": "Achraf Hakimi", "position": "Right-Back", "nationality": "Morocco", "shirt_number": 2, "birthdate": "1998-11-04"},
        {"name": "Ivan Perišić", "position": "Left Winger", "nationality": "Croatia", "shirt_number": 44, "birthdate": "1989-02-02"},
        {"name": "Christian Eriksen", "position": "Attacking Midfield", "nationality": "Denmark", "shirt_number": 24, "birthdate": "1992-02-14"},
        {"name": "Stefan de Vrij", "position": "Centre-Back", "nationality": "Netherlands", "shirt_number": 6, "birthdate": "1992-02-05"},
        {"name": "Matteo Darmian", "position": "Right-Back", "nationality": "Italy", "shirt_number": 36, "birthdate": "1989-12-02"},
        {"name": "Arturo Vidal", "position": "Central Midfield", "nationality": "Chile", "shirt_number": 22, "birthdate": "1987-05-22"},
        {"name": "Alexis Sánchez", "position": "Left Winger", "nationality": "Chile", "shirt_number": 7, "birthdate": "1988-12-19"},
        {"name": "Roberto Gagliardini", "position": "Central Midfield", "nationality": "Italy", "shirt_number": 5, "birthdate": "1994-01-07"}
    ]
    
    # Lấy các đội
    cur.execute("""
        SELECT t.id, t.name, l.name as league_name
        FROM teams t
        LEFT JOIN leagues l ON l.id = t.league_id
        WHERE (l.name = 'Bundesliga' AND t.name = 'Bayern Munich') OR
              (l.name = 'Serie A' AND t.name IN ('AC Milan', 'Inter Milan'))
        ORDER BY t.name
    """)
    
    teams = cur.fetchall()
    
    # Thêm cầu thủ cho Bayern Munich
    bayern_team = next((t for t in teams if 'Bayern Munich' in t[1]), None)
    if bayern_team:
        print(f"\n⚽ Thêm cầu thủ cho Bayern Munich...")
        for player in bayern_players:
            cur.execute("""
                INSERT OR IGNORE INTO players(
                    team_id, name, nationality, position, shirt_number, birthdate, external_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                bayern_team[0],
                player['name'],
                player['nationality'],
                player['position'],
                player['shirt_number'],
                player['birthdate'],
                f"bayern_{player['name'].replace(' ', '_').lower()}"
            ))
        print(f"  ✅ Đã thêm {len(bayern_players)} cầu thủ cho Bayern Munich")
    
    # Thêm cầu thủ cho AC Milan
    ac_milan_team = next((t for t in teams if 'AC Milan' in t[1]), None)
    if ac_milan_team:
        print(f"\n⚽ Thêm cầu thủ cho AC Milan...")
        for player in ac_milan_players:
            cur.execute("""
                INSERT OR IGNORE INTO players(
                    team_id, name, nationality, position, shirt_number, birthdate, external_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ac_milan_team[0],
                player['name'],
                player['nationality'],
                player['position'],
                player['shirt_number'],
                player['birthdate'],
                f"acmilan_{player['name'].replace(' ', '_').lower()}"
            ))
        print(f"  ✅ Đã thêm {len(ac_milan_players)} cầu thủ cho AC Milan")
    
    # Thêm cầu thủ cho Inter Milan
    inter_milan_team = next((t for t in teams if 'Inter Milan' in t[1]), None)
    if inter_milan_team:
        print(f"\n⚽ Thêm cầu thủ cho Inter Milan...")
        for player in inter_milan_players:
            cur.execute("""
                INSERT OR IGNORE INTO players(
                    team_id, name, nationality, position, shirt_number, birthdate, external_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                inter_milan_team[0],
                player['name'],
                player['nationality'],
                player['position'],
                player['shirt_number'],
                player['birthdate'],
                f"inter_{player['name'].replace(' ', '_').lower()}"
            ))
        print(f"  ✅ Đã thêm {len(inter_milan_players)} cầu thủ cho Inter Milan")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Hoàn thành! Đã thêm cầu thủ sao cho các đội lớn khác")

if __name__ == "__main__":
    add_more_star_players()

