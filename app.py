# app.py
from flask import Flask, render_template, jsonify, g, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import db, sqlite3
import auth
from decorators import admin_required, login_required_custom, user_or_admin_required

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return auth.User.get(user_id)

def get_conn():
    return db.get_db_connection()

@app.route("/")
def index():
    conn = get_conn()
    cur = conn.cursor()
    
    # Lấy dữ liệu cho trang chủ
    cur.execute("SELECT COUNT(*) as count FROM leagues")
    leagues_count = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM teams")
    teams_count = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM players")
    players_count = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM matches")
    matches_count = cur.fetchone()['count']
    
    # Lấy danh sách leagues
    cur.execute("SELECT * FROM leagues LIMIT 6")
    leagues = [dict(row) for row in cur.fetchall()]
    
    # Lấy recent matches
    cur.execute("""
        SELECT m.*, l.name as league_name, 
               t1.name as home_team, t2.name as away_team
        FROM matches m
        LEFT JOIN leagues l ON l.id = m.league_id
        LEFT JOIN teams t1 ON t1.id = m.home_team_id
        LEFT JOIN teams t2 ON t2.id = m.away_team_id
        ORDER BY m.match_date DESC LIMIT 10
    """)
    recent_matches = [dict(row) for row in cur.fetchall()]
    
    conn.close()
    
    return render_template("index.html", 
                         leagues=leagues,
                         recent_matches=recent_matches,
                         stats={
                             'leagues': leagues_count,
                             'teams': teams_count,
                             'players': players_count,
                             'matches': matches_count
                         })

@app.route("/league/<int:league_id>")
def league_page(league_id):
    conn = get_conn()
    cur = conn.cursor()
    
    # Lấy thông tin league
    cur.execute("SELECT * FROM leagues WHERE id=?", (league_id,))
    league = cur.fetchone()
    if not league:
        conn.close()
        return "League not found", 404
    
    league = dict(league)
    
    # Lấy teams trong league
    cur.execute("SELECT * FROM teams WHERE league_id=?", (league_id,))
    teams = [dict(row) for row in cur.fetchall()]
    
    # Lấy recent matches
    cur.execute("""
        SELECT m.*, t1.name as home_team, t2.name as away_team
        FROM matches m
        LEFT JOIN teams t1 ON t1.id = m.home_team_id
        LEFT JOIN teams t2 ON t2.id = m.away_team_id
        WHERE m.league_id = ?
        ORDER BY m.match_date DESC LIMIT 10
    """, (league_id,))
    matches = [dict(row) for row in cur.fetchall()]
    
    conn.close()
    
    return render_template("league.html", league=league, teams=teams, matches=matches)

@app.route("/team/<int:team_id>")
def team_page(team_id):
    conn = get_conn()
    cur = conn.cursor()

    # Lấy thông tin team
    cur.execute("SELECT * FROM teams WHERE id=?", (team_id,))
    team = cur.fetchone()
    if not team:
        conn.close()
        return "Team not found", 404

    team = dict(team)

    # Lấy league info
    cur.execute("SELECT * FROM leagues WHERE id=?", (team['league_id'],))
    league = cur.fetchone()
    league = dict(league) if league else None

    # Lấy players của team
    cur.execute("SELECT * FROM players WHERE team_id=?", (team_id,))
    players = [dict(row) for row in cur.fetchall()]

    # Lấy recent matches
    cur.execute("""
        SELECT m.*, t1.name as home_team, t2.name as away_team
        FROM matches m
        LEFT JOIN teams t1 ON t1.id = m.home_team_id
        LEFT JOIN teams t2 ON t2.id = m.away_team_id
        WHERE m.home_team_id = ? OR m.away_team_id = ?
        ORDER BY m.match_date DESC LIMIT 10
    """, (team_id, team_id))
    matches = [dict(row) for row in cur.fetchall()]

    conn.close()

    return render_template("team.html", team=team, league=league, players=players, matches=matches)

@app.route("/player/<int:player_id>")
def player_page(player_id):
    conn = get_conn()
    cur = conn.cursor()

    # Lấy thông tin player
    cur.execute("SELECT * FROM players WHERE id=?", (player_id,))
    player = cur.fetchone()
    if not player:
        conn.close()
        return "Player not found", 404

    player = dict(player)

    # Lấy team info
    cur.execute("SELECT * FROM teams WHERE id=?", (player['team_id'],))
    team = cur.fetchone()
    team = dict(team) if team else None

    # Lấy league info
    if team:
        cur.execute("SELECT * FROM leagues WHERE id=?", (team['league_id'],))
        league = cur.fetchone()
        league = dict(league) if league else None
    else:
        league = None

    conn.close()

    return render_template("player.html", player=player, team=team, league=league)

# API endpoints for frontend JS
@app.route("/api/leagues")
def api_leagues():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, country_code, external_id FROM leagues")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route("/api/leagues/<int:league_id>/teams")
def api_league_teams(league_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, short_name, external_id FROM teams WHERE league_id=?", (league_id,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route("/api/teams/<int:team_id>")
def api_team(team_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM teams WHERE id=?", (team_id,))
    r = cur.fetchone()
    team = dict(r) if r else {}
    # recent matches
    cur.execute("""SELECT m.id,m.match_date,m.home_score,m.away_score, t1.name AS home, t2.name AS away
                   FROM matches m
                   LEFT JOIN teams t1 ON t1.id=m.home_team_id
                   LEFT JOIN teams t2 ON t2.id=m.away_team_id
                   WHERE m.home_team_id=? OR m.away_team_id=?
                   ORDER BY m.match_date DESC LIMIT 10""", (team_id, team_id))
    matches = [dict(x) for x in cur.fetchall()]
    conn.close()
    return jsonify({"team": team, "matches": matches})

@app.route("/api/teams/<int:team_id>/players")
def api_team_players(team_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,position,shirt_number,nationality FROM players WHERE team_id=?", (team_id,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route("/api/players/<int:player_id>")
def api_player(player_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM players WHERE id=?", (player_id,))
    r = cur.fetchone()
    conn.close()
    return jsonify(dict(r) if r else {})

# Authentication routes
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = auth.User.verify_password(username, password)
        if user:
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Chào mừng {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng.', 'error')
    
    return render_template('auth/login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp.', 'error')
            return render_template('auth/register.html')
        
        if auth.User.create_user(username, email, password):
            flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Tên đăng nhập hoặc email đã tồn tại.', 'error')
    
    return render_template('auth/register.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất thành công.', 'info')
    return redirect(url_for('index'))

@app.route("/dashboard")
@admin_required
def dashboard():
    users = db.get_all_users()
    return render_template('dashboard.html', users=users)

@app.route("/profile")
@login_required_custom
def profile():
    return render_template('auth/profile.html', user=current_user)

# Admin API endpoints
@app.route("/api/admin/users")
@admin_required
def api_admin_users():
    users = db.get_all_users()
    return jsonify(users)

@app.route("/api/admin/users/<int:user_id>/role", methods=['PUT'])
@admin_required
def api_update_user_role(user_id):
    data = request.get_json()
    new_role = data.get('role')
    
    if new_role not in ['admin', 'user']:
        return jsonify({'error': 'Role không hợp lệ'}), 400
    
    db.update_user_role(user_id, new_role)
    return jsonify({'success': True})

@app.route("/api/admin/users/<int:user_id>", methods=['DELETE'])
@admin_required
def api_delete_user(user_id):
    if user_id == current_user.id:
        return jsonify({'error': 'Không thể xóa chính mình'}), 400
    
    db.delete_user(user_id)
    return jsonify({'success': True})

if __name__ == "__main__":
    db.init_db()
    app.run(debug=True, port=5000)
