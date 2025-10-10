# add_sample_data.py - Thêm dữ liệu mẫu vào database
import db

def add_sample_data():
    """Thêm dữ liệu mẫu vào database"""
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    print("🚀 Thêm dữ liệu mẫu...")
    
    # Thêm leagues
    leagues_data = [
        (2021, "Premier League", "EN"),
        (2014, "La Liga", "ES"),
        (2002, "Bundesliga", "DE"),
        (2019, "Serie A", "IT"),
        (2015, "Ligue 1", "FR"),
        (2017, "Primeira Liga", "PT")
    ]
    
    for external_id, name, country_code in leagues_data:
        cur.execute("INSERT OR IGNORE INTO leagues (external_id, name, country_code) VALUES (?, ?, ?)",
                   (external_id, name, country_code))
    
    print("✅ Đã thêm leagues")
    
    # Thêm teams
    teams_data = [
        # Premier League
        (1, 2021, "Manchester United", "MUN", 1878, "Old Trafford"),
        (2, 2021, "Manchester City", "MCI", 1880, "Etihad Stadium"),
        (3, 2021, "Liverpool", "LIV", 1892, "Anfield"),
        (4, 2021, "Chelsea", "CHE", 1905, "Stamford Bridge"),
        (5, 2021, "Arsenal", "ARS", 1886, "Emirates Stadium"),
        (6, 2021, "Tottenham", "TOT", 1882, "Tottenham Hotspur Stadium"),
        
        # La Liga
        (7, 2014, "Real Madrid", "RMA", 1902, "Santiago Bernabéu"),
        (8, 2014, "Barcelona", "BAR", 1899, "Camp Nou"),
        (9, 2014, "Atletico Madrid", "ATM", 1903, "Wanda Metropolitano"),
        (10, 2014, "Sevilla", "SEV", 1890, "Ramón Sánchez-Pizjuán"),
        
        # Bundesliga
        (11, 2002, "Bayern Munich", "BAY", 1900, "Allianz Arena"),
        (12, 2002, "Borussia Dortmund", "BVB", 1909, "Signal Iduna Park"),
        (13, 2002, "RB Leipzig", "RBL", 2009, "Red Bull Arena"),
        
        # Serie A
        (14, 2019, "Juventus", "JUV", 1897, "Allianz Stadium"),
        (15, 2019, "AC Milan", "MIL", 1899, "San Siro"),
        (16, 2019, "Inter Milan", "INT", 1908, "San Siro"),
        (17, 2019, "Napoli", "NAP", 1926, "Stadio Diego Armando Maradona"),
        
        # Ligue 1
        (18, 2015, "Paris Saint-Germain", "PSG", 1970, "Parc des Princes"),
        (19, 2015, "Olympique Marseille", "OM", 1899, "Stade Vélodrome"),
        (20, 2015, "Lyon", "OL", 1950, "Groupama Stadium")
    ]
    
    for external_id, league_external_id, name, short_name, founded, stadium in teams_data:
        cur.execute("""
            INSERT OR IGNORE INTO teams (external_id, league_id, name, short_name, founded_year, stadium)
            VALUES (?, (SELECT id FROM leagues WHERE external_id = ?), ?, ?, ?, ?)
        """, (external_id, league_external_id, name, short_name, founded, stadium))
    
    print("✅ Đã thêm teams")
    
    # Thêm players
    players_data = [
        # Manchester United
        (1, 1, "Marcus Rashford", "England", "Forward", 10, "1997-10-31"),
        (2, 1, "Bruno Fernandes", "Portugal", "Midfielder", 18, "1994-09-08"),
        (3, 1, "Harry Maguire", "England", "Defender", 5, "1993-03-05"),
        
        # Manchester City
        (4, 2, "Erling Haaland", "Norway", "Forward", 9, "2000-07-21"),
        (5, 2, "Kevin De Bruyne", "Belgium", "Midfielder", 17, "1991-06-28"),
        (6, 2, "Ruben Dias", "Portugal", "Defender", 3, "1997-05-14"),
        
        # Liverpool
        (7, 3, "Mohamed Salah", "Egypt", "Forward", 11, "1992-06-15"),
        (8, 3, "Virgil van Dijk", "Netherlands", "Defender", 4, "1991-07-08"),
        (9, 3, "Sadio Mané", "Senegal", "Forward", 10, "1992-04-10"),
        
        # Real Madrid
        (10, 7, "Karim Benzema", "France", "Forward", 9, "1987-12-19"),
        (11, 7, "Luka Modrić", "Croatia", "Midfielder", 10, "1985-09-09"),
        (12, 7, "Sergio Ramos", "Spain", "Defender", 4, "1986-03-30"),
        
        # Barcelona
        (13, 8, "Lionel Messi", "Argentina", "Forward", 10, "1987-06-24"),
        (14, 8, "Pedri", "Spain", "Midfielder", 16, "2002-11-25"),
        (15, 8, "Gerard Piqué", "Spain", "Defender", 3, "1987-02-02"),
        
        # Bayern Munich
        (16, 11, "Robert Lewandowski", "Poland", "Forward", 9, "1988-08-21"),
        (17, 11, "Thomas Müller", "Germany", "Midfielder", 25, "1989-09-13"),
        (18, 11, "Manuel Neuer", "Germany", "Goalkeeper", 1, "1986-03-27"),
        
        # Juventus
        (19, 14, "Cristiano Ronaldo", "Portugal", "Forward", 7, "1985-02-05"),
        (20, 14, "Paulo Dybala", "Argentina", "Forward", 10, "1993-11-15"),
        (21, 14, "Giorgio Chiellini", "Italy", "Defender", 3, "1984-08-14"),
        
        # PSG
        (22, 18, "Kylian Mbappé", "France", "Forward", 7, "1998-12-20"),
        (23, 18, "Neymar Jr", "Brazil", "Forward", 10, "1992-02-05"),
        (24, 18, "Marquinhos", "Brazil", "Defender", 5, "1994-05-14")
    ]
    
    for external_id, team_external_id, name, nationality, position, shirt_number, birthdate in players_data:
        cur.execute("""
            INSERT OR IGNORE INTO players (external_id, team_id, name, nationality, position, shirt_number, birthdate)
            VALUES (?, (SELECT id FROM teams WHERE external_id = ?), ?, ?, ?, ?, ?)
        """, (external_id, team_external_id, name, nationality, position, shirt_number, birthdate))
    
    print("✅ Đã thêm players")
    
    # Thêm matches
    matches_data = [
        # Premier League matches
        (1, 2021, "2023/2024", "2024-01-15", 1, 2, 2, 1),  # Man Utd vs Man City
        (2, 2021, "2023/2024", "2024-01-20", 3, 4, 3, 0),  # Liverpool vs Chelsea
        (3, 2021, "2023/2024", "2024-01-25", 5, 6, 1, 2),  # Arsenal vs Tottenham
        
        # La Liga matches
        (4, 2014, "2023/2024", "2024-01-18", 7, 8, 2, 1),  # Real Madrid vs Barcelona
        (5, 2014, "2023/2024", "2024-01-22", 9, 10, 1, 1), # Atletico vs Sevilla
        
        # Bundesliga matches
        (6, 2002, "2023/2024", "2024-01-16", 11, 12, 4, 2), # Bayern vs Dortmund
        (7, 2002, "2023/2024", "2024-01-24", 13, 11, 0, 3), # Leipzig vs Bayern
        
        # Serie A matches
        (8, 2019, "2023/2024", "2024-01-19", 14, 15, 2, 0), # Juventus vs Milan
        (9, 2019, "2023/2024", "2024-01-23", 16, 17, 1, 3), # Inter vs Napoli
        
        # Ligue 1 matches
        (10, 2015, "2023/2024", "2024-01-17", 18, 19, 3, 1), # PSG vs Marseille
        (11, 2015, "2023/2024", "2024-01-21", 20, 18, 0, 2), # Lyon vs PSG
    ]
    
    for external_id, league_external_id, season, match_date, home_team_ext_id, away_team_ext_id, home_score, away_score in matches_data:
        cur.execute("""
            INSERT OR IGNORE INTO matches (external_id, league_id, season, match_date, home_team_id, away_team_id, home_score, away_score)
            VALUES (?, (SELECT id FROM leagues WHERE external_id = ?), ?, ?, 
                   (SELECT id FROM teams WHERE external_id = ?), 
                   (SELECT id FROM teams WHERE external_id = ?), ?, ?)
        """, (external_id, league_external_id, season, match_date, home_team_ext_id, away_team_ext_id, home_score, away_score))
    
    print("✅ Đã thêm matches")
    
    conn.commit()
    conn.close()
    
    print("\n🎉 Hoàn thành thêm dữ liệu mẫu!")
    print("📊 Thống kê:")
    print(f"   - Leagues: {len(leagues_data)}")
    print(f"   - Teams: {len(teams_data)}")
    print(f"   - Players: {len(players_data)}")
    print(f"   - Matches: {len(matches_data)}")

if __name__ == "__main__":
    db.init_db()
    add_sample_data()
