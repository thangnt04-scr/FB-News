# add_missing_teams.py - Thêm teams còn thiếu cho các giải chính
import db

def add_missing_teams():
    """Thêm teams còn thiếu cho La Liga, Bundesliga, Serie A"""
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    print("🔧 THÊM TEAMS CÒN THIẾU CHO CÁC GIẢI CHÍNH")
    print("=" * 60)
    
    # Lấy league IDs
    cur.execute("SELECT id, name FROM leagues WHERE name IN ('La Liga', 'Bundesliga', 'Serie A')")
    leagues = {row['name']: row['id'] for row in cur.fetchall()}
    
    # Teams cần thêm cho La Liga
    la_liga_teams = [
        {"name": "Sevilla FC", "short_name": "SEV", "founded": 1890, "stadium": "Ramón Sánchez-Pizjuán", "external_id": 559},
        {"name": "Valencia CF", "short_name": "VAL", "founded": 1919, "stadium": "Mestalla", "external_id": 95},
        {"name": "Villarreal CF", "short_name": "VIL", "founded": 1923, "stadium": "Estadio de la Cerámica", "external_id": 94},
        {"name": "Real Sociedad", "short_name": "RSO", "founded": 1909, "stadium": "Anoeta", "external_id": 92},
        {"name": "Real Betis", "short_name": "BET", "founded": 1907, "stadium": "Benito Villamarín", "external_id": 90},
        {"name": "Athletic Bilbao", "short_name": "ATH", "founded": 1898, "stadium": "San Mamés", "external_id": 77},
        {"name": "Celta Vigo", "short_name": "CEL", "founded": 1923, "stadium": "Balaídos", "external_id": 558},
        {"name": "Mallorca", "short_name": "MAL", "founded": 1916, "stadium": "Son Moix", "external_id": 89},
        {"name": "Getafe CF", "short_name": "GET", "founded": 1983, "stadium": "Coliseum Alfonso Pérez", "external_id": 82},
        {"name": "Osasuna", "short_name": "OSA", "founded": 1920, "stadium": "El Sadar", "external_id": 79},
        {"name": "Girona FC", "short_name": "GIR", "founded": 1930, "stadium": "Montilivi", "external_id": 298},
        {"name": "Rayo Vallecano", "short_name": "RAY", "founded": 1924, "stadium": "Vallecas", "external_id": 87},
        {"name": "Alavés", "short_name": "ALA", "founded": 1921, "stadium": "Mendizorroza", "external_id": 263},
        {"name": "Cádiz CF", "short_name": "CAD", "founded": 1910, "stadium": "Nuevo Mirandilla", "external_id": 264},
        {"name": "Las Palmas", "short_name": "LPA", "founded": 1949, "stadium": "Gran Canaria", "external_id": 275},
        {"name": "Almería", "short_name": "ALM", "founded": 1989, "stadium": "Power Horse Stadium", "external_id": 267},
        {"name": "Granada CF", "short_name": "GRA", "founded": 1931, "stadium": "Nuevo Los Cármenes", "external_id": 83}
    ]
    
    # Teams cần thêm cho Bundesliga
    bundesliga_teams = [
        {"name": "Bayern Munich", "short_name": "FCB", "founded": 1900, "stadium": "Allianz Arena", "external_id": 5},
        {"name": "Borussia Dortmund", "short_name": "BVB", "founded": 1909, "stadium": "Signal Iduna Park", "external_id": 4},
        {"name": "Bayer Leverkusen", "short_name": "B04", "founded": 1904, "stadium": "BayArena", "external_id": 3},
        {"name": "RB Leipzig", "short_name": "RBL", "founded": 2009, "stadium": "Red Bull Arena", "external_id": 721},
        {"name": "VfB Stuttgart", "short_name": "VFB", "founded": 1893, "stadium": "Mercedes-Benz Arena", "external_id": 10},
        {"name": "Eintracht Frankfurt", "short_name": "SGE", "founded": 1899, "stadium": "Deutsche Bank Park", "external_id": 19},
        {"name": "SC Freiburg", "short_name": "SCF", "founded": 1904, "stadium": "Europa-Park Stadion", "external_id": 17},
        {"name": "Borussia Mönchengladbach", "short_name": "BMG", "founded": 1900, "stadium": "Borussia-Park", "external_id": 18},
        {"name": "VfL Wolfsburg", "short_name": "WOB", "founded": 1945, "stadium": "Volkswagen Arena", "external_id": 11},
        {"name": "Werder Bremen", "short_name": "SVW", "founded": 1899, "stadium": "Weserstadion", "external_id": 12},
        {"name": "FC Augsburg", "short_name": "FCA", "founded": 1907, "stadium": "WWK Arena", "external_id": 16},
        {"name": "1. FC Union Berlin", "short_name": "FCU", "founded": 1966, "stadium": "Stadion An der Alten Försterei", "external_id": 1},
        {"name": "1. FC Köln", "short_name": "KOE", "founded": 1948, "stadium": "RheinEnergieStadion", "external_id": 1},
        {"name": "1. FSV Mainz 05", "short_name": "M05", "founded": 1905, "stadium": "Opel Arena", "external_id": 1},
        {"name": "TSG Hoffenheim", "short_name": "TSG", "founded": 1899, "stadium": "PreZero Arena", "external_id": 2},
        {"name": "1. FC Heidenheim", "short_name": "FCH", "founded": 1846, "stadium": "Voith-Arena", "external_id": 1},
        {"name": "VfL Bochum", "short_name": "BOC", "founded": 1848, "stadium": "Vonovia Ruhrstadion", "external_id": 36},
        {"name": "SV Darmstadt 98", "short_name": "SVD", "founded": 1898, "stadium": "Merck-Stadion am Böllenfalltor", "external_id": 55}
    ]
    
    # Teams cần thêm cho Serie A
    serie_a_teams = [
        {"name": "AC Milan", "short_name": "MIL", "founded": 1899, "stadium": "San Siro", "external_id": 98},
        {"name": "Inter Milan", "short_name": "INT", "founded": 1908, "stadium": "San Siro", "external_id": 108},
        {"name": "Napoli", "short_name": "NAP", "founded": 1926, "stadium": "Diego Armando Maradona", "external_id": 113},
        {"name": "AS Roma", "short_name": "ROM", "founded": 1927, "stadium": "Stadio Olimpico", "external_id": 100},
        {"name": "Atalanta", "short_name": "ATA", "founded": 1907, "stadium": "Gewiss Stadium", "external_id": 102},
        {"name": "Lazio", "short_name": "LAZ", "founded": 1900, "stadium": "Stadio Olimpico", "external_id": 110},
        {"name": "Fiorentina", "short_name": "FIO", "founded": 1926, "stadium": "Artemio Franchi", "external_id": 99},
        {"name": "Bologna", "short_name": "BOL", "founded": 1909, "stadium": "Renato Dall'Ara", "external_id": 103},
        {"name": "Torino", "short_name": "TOR", "founded": 1906, "stadium": "Stadio Olimpico Grande Torino", "external_id": 586},
        {"name": "Genoa", "short_name": "GEN", "founded": 1893, "stadium": "Luigi Ferraris", "external_id": 107},
        {"name": "Cagliari", "short_name": "CAG", "founded": 1920, "stadium": "Sardegna Arena", "external_id": 104},
        {"name": "Udinese", "short_name": "UDI", "founded": 1896, "stadium": "Dacia Arena", "external_id": 115},
        {"name": "Sassuolo", "short_name": "SAS", "founded": 1920, "stadium": "Mapei Stadium", "external_id": 471},
        {"name": "Lecce", "short_name": "LEC", "founded": 1908, "stadium": "Via del Mare", "external_id": 5890},
        {"name": "Hellas Verona", "short_name": "VER", "founded": 1903, "stadium": "Marc'Antonio Bentegodi", "external_id": 450},
        {"name": "Empoli", "short_name": "EMP", "founded": 1920, "stadium": "Carlo Castellani", "external_id": 445},
        {"name": "Salernitana", "short_name": "SAL", "founded": 1919, "stadium": "Arechi", "external_id": 455},
        {"name": "Frosinone", "short_name": "FRO", "founded": 1906, "stadium": "Benito Stirpe", "external_id": 470},
        {"name": "Monza", "short_name": "MON", "founded": 1912, "stadium": "U-Power Stadium", "external_id": 5911}
    ]
    
    # Thêm teams cho La Liga
    if 'La Liga' in leagues:
        print(f"\n🏆 Thêm teams cho La Liga...")
        for team in la_liga_teams:
            cur.execute("""
                INSERT OR IGNORE INTO teams(league_id, name, short_name, founded_year, stadium, external_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (leagues['La Liga'], team['name'], team['short_name'], team['founded'], team['stadium'], team['external_id']))
        print(f"✅ Đã thêm {len(la_liga_teams)} teams cho La Liga")
    
    # Thêm teams cho Bundesliga
    if 'Bundesliga' in leagues:
        print(f"\n🏆 Thêm teams cho Bundesliga...")
        for team in bundesliga_teams:
            cur.execute("""
                INSERT OR IGNORE INTO teams(league_id, name, short_name, founded_year, stadium, external_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (leagues['Bundesliga'], team['name'], team['short_name'], team['founded'], team['stadium'], team['external_id']))
        print(f"✅ Đã thêm {len(bundesliga_teams)} teams cho Bundesliga")
    
    # Thêm teams cho Serie A
    if 'Serie A' in leagues:
        print(f"\n🏆 Thêm teams cho Serie A...")
        for team in serie_a_teams:
            cur.execute("""
                INSERT OR IGNORE INTO teams(league_id, name, short_name, founded_year, stadium, external_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (leagues['Serie A'], team['name'], team['short_name'], team['founded'], team['stadium'], team['external_id']))
        print(f"✅ Đã thêm {len(serie_a_teams)} teams cho Serie A")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Hoàn thành! Đã thêm teams còn thiếu cho các giải chính")

if __name__ == "__main__":
    add_missing_teams()

