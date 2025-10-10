import time
from services.football_api import (
    fetch_competitions,
    fetch_teams_for_competition,
    fetch_team,
    fetch_matches_for_competition,
)
from db import get_db_connection, init_db

# Danh sách giải cần sync (ID lấy từ football-data.org)
TARGET_COMPETITIONS = {
    2021: "Premier League",     # Anh
    2015: "Ligue 1",            # Pháp
    2002: "Bundesliga",         # Đức
    2019: "Serie A",            # Ý
    2014: "La Liga",            # Tây Ban Nha
    2017: "Primeira Liga",      # Bồ Đào Nha
    2003: "Eredivisie",         # Hà Lan
    # ⚠️ football-data.org không có V-League
}

def sync():
    init_db()
    conn = get_db_connection()
    cur = conn.cursor()

    print("🔍 Fetch competitions...")
    comps = fetch_competitions().get("competitions", [])
    comp_map = {c["id"]: c["name"] for c in comps if c["id"] in TARGET_COMPETITIONS}

    print(f"✅ Found competitions: {list(comp_map.items())}")

    for comp_id, comp_name in comp_map.items():
        print(f"\n⚽ Sync league: {comp_name}")
        teams_data = fetch_teams_for_competition(comp_id).get("teams", [])

        for t in teams_data:
            team_id = t["id"]
            team_name = t["name"]

            # check nếu team đã có trong DB
            cur.execute("SELECT id FROM teams WHERE external_id = ?", (team_id,))
            if cur.fetchone():
                print(f"  ⏩ Skip (already in DB): {team_name}")
                continue

            print(f"  🏟️ Team: {team_name}")
            try:
                team_detail = fetch_team(team_id)
            except Exception as e:
                print(f"    ❌ failed fetching team detail: {e}")
                continue

            # Insert team
            cur.execute(
                """
                INSERT OR IGNORE INTO teams(league_id, name, short_name, founded_year, stadium, external_id)
                VALUES ((SELECT id FROM leagues WHERE external_id=?), ?, ?, ?, ?, ?)
                """,
                (
                    comp_id,
                    team_detail.get("name"),
                    team_detail.get("shortName"),
                    team_detail.get("founded"),
                    team_detail.get("venue"),
                    team_detail.get("id"),
                ),
            )
            conn.commit()

            # Insert players
            squad = team_detail.get("squad", [])
            for p in squad:
                cur.execute(
                    """
                    INSERT OR IGNORE INTO players(
                        team_id, name, nationality, position, shirt_number, birthdate, external_id
                    )
                    VALUES (
                        (SELECT id FROM teams WHERE external_id=?),
                        ?, ?, ?, ?, ?, ?
                    )
                    """,
                    (
                        team_id,
                        p.get("name"),
                        p.get("nationality"),
                        p.get("position"),
                        p.get("shirtNumber"),
                        p.get("dateOfBirth"),
                        p.get("id"),
                    ),
                )
            conn.commit()

        # Insert matches
        try:
            matches_data = fetch_matches_for_competition(comp_id).get("matches", [])
        except Exception as e:
            print(f"    ❌ failed fetching matches: {e}")
            matches_data = []

        for m in matches_data:
            cur.execute(
                """
                INSERT OR IGNORE INTO matches(
                    league_id, season, match_date, home_team_id, away_team_id, home_score, away_score
                )
                VALUES (
                    (SELECT id FROM leagues WHERE external_id=?),
                    ?, ?, 
                    (SELECT id FROM teams WHERE external_id=?),
                    (SELECT id FROM teams WHERE external_id=?),
                    ?, ?
                )
                """,
                (
                    comp_id,
                    m.get("season", {}).get("startDate", "2023/2024"),
                    m.get("utcDate"),
                    m.get("homeTeam", {}).get("id"),
                    m.get("awayTeam", {}).get("id"),
                    m.get("score", {}).get("fullTime", {}).get("home"),
                    m.get("score", {}).get("fullTime", {}).get("away"),
                ),
            )
        conn.commit()

    conn.close()
    print("\n🎉 Sync completed!")

if __name__ == "__main__":
    sync()
