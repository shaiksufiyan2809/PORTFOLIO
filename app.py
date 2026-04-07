from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import mysql.connector
import hashlib
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'jamsheer_portfolio_secret_2025')

# ─── DB Config ────────────────────────────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sufiyan@2006',   # <-- change this
    'database': 'portfolio_db'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def query(sql, params=None, fetchone=False):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ())
    result = cur.fetchone() if fetchone else cur.fetchall()
    conn.close()
    return result

def execute(sql, params=None):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    last_id = cur.lastrowid
    conn.commit()
    conn.close()
    return last_id

# ─── Auth Decorator ───────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# ─── Public Routes ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/portfolio')
def portfolio_data():
    hero         = query("SELECT * FROM hero LIMIT 1", fetchone=True)
    education    = query("SELECT * FROM education ORDER BY display_order")
    skills       = query("SELECT * FROM skills ORDER BY display_order")
    projects     = query("SELECT * FROM projects ORDER BY display_order")
    achievements = query("SELECT * FROM achievements ORDER BY display_order")
    certs        = query("SELECT * FROM certifications")

    # Group skills by category
    skills_grouped = {}
    for s in skills:
        skills_grouped.setdefault(s['category'], []).append(s['skill_name'])

    return jsonify({
        'hero': hero,
        'education': education,
        'skills': skills_grouped,
        'projects': projects,
        'achievements': achievements,
        'certifications': certs
    })

# ─── Admin Auth ───────────────────────────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        hashed = hashlib.sha256(password.encode()).hexdigest()
        admin = query("SELECT * FROM admin WHERE username=%s AND password_hash=%s",
                      (username, hashed), fetchone=True)
        if admin:
            session['admin_logged_in'] = True
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    return render_template('admin.html')

@app.route('/admin/check-auth')
def check_auth():
    if session.get('admin_logged_in'):
        return jsonify({'ok': True})
    return jsonify({'ok': False}), 401

def admin_logout():
    session.clear()
    return redirect('/')

# ─── Admin Panel Page ─────────────────────────────────────────────────────────
@app.route('/admin')
@login_required
def admin_panel():
    return render_template('admin.html')

# ─── Admin API — Hero ─────────────────────────────────────────────────────────
@app.route('/admin/api/hero', methods=['PUT'])
@login_required
def update_hero():
    d = request.get_json()
    execute("""UPDATE hero SET name=%s, tagline=%s, bio=%s, email=%s,
               phone=%s, location=%s, github_url=%s, linkedin_url=%s,
               leetcode_url=%s, resume_url=%s WHERE id=1""",
            (d['name'], d['tagline'], d['bio'], d['email'],
             d['phone'], d['location'], d['github_url'],
             d['linkedin_url'], d['leetcode_url'], d.get('resume_url','')))
    return jsonify({'success': True})

# ─── Admin API — Education ────────────────────────────────────────────────────
@app.route('/admin/api/education', methods=['POST'])
@login_required
def add_education():
    d = request.get_json()
    execute("INSERT INTO education (degree,institution,year_range,score,score_label,display_order) VALUES (%s,%s,%s,%s,%s,%s)",
            (d['degree'],d['institution'],d['year_range'],d['score'],d.get('score_label','CGPA'),d.get('display_order',0)))
    return jsonify({'success': True})

@app.route('/admin/api/education/<int:eid>', methods=['PUT','DELETE'])
@login_required
def edit_education(eid):
    if request.method == 'DELETE':
        execute("DELETE FROM education WHERE id=%s", (eid,))
        return jsonify({'success': True})
    d = request.get_json()
    execute("UPDATE education SET degree=%s,institution=%s,year_range=%s,score=%s,score_label=%s WHERE id=%s",
            (d['degree'],d['institution'],d['year_range'],d['score'],d.get('score_label','CGPA'),eid))
    return jsonify({'success': True})

# ─── Admin API — Skills ───────────────────────────────────────────────────────
@app.route('/admin/api/skills', methods=['POST'])
@login_required
def add_skill():
    d = request.get_json()
    execute("INSERT INTO skills (category,skill_name,display_order) VALUES (%s,%s,%s)",
            (d['category'],d['skill_name'],d.get('display_order',0)))
    return jsonify({'success': True})

@app.route('/admin/api/skills/<int:sid>', methods=['DELETE'])
@login_required
def delete_skill(sid):
    execute("DELETE FROM skills WHERE id=%s", (sid,))
    return jsonify({'success': True})

# ─── Admin API — Projects ─────────────────────────────────────────────────────
@app.route('/admin/api/projects', methods=['POST'])
@login_required
def add_project():
    d = request.get_json()
    execute("INSERT INTO projects (title,description,tech_stack,github_url,live_url,highlight,display_order) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (d['title'],d['description'],d['tech_stack'],d.get('github_url',''),d.get('live_url',''),d.get('highlight',False),d.get('display_order',0)))
    return jsonify({'success': True})

@app.route('/admin/api/projects/<int:pid>', methods=['PUT','DELETE'])
@login_required
def edit_project(pid):
    if request.method == 'DELETE':
        execute("DELETE FROM projects WHERE id=%s", (pid,))
        return jsonify({'success': True})
    d = request.get_json()
    execute("UPDATE projects SET title=%s,description=%s,tech_stack=%s,github_url=%s,live_url=%s,highlight=%s WHERE id=%s",
            (d['title'],d['description'],d['tech_stack'],d.get('github_url',''),d.get('live_url',''),d.get('highlight',False),pid))
    return jsonify({'success': True})

# ─── Admin API — Achievements ─────────────────────────────────────────────────
@app.route('/admin/api/achievements', methods=['POST'])
@login_required
def add_achievement():
    d = request.get_json()
    execute("INSERT INTO achievements (title,description,icon,display_order) VALUES (%s,%s,%s,%s)",
            (d['title'],d['description'],d.get('icon','🏆'),d.get('display_order',0)))
    return jsonify({'success': True})

@app.route('/admin/api/achievements/<int:aid>', methods=['PUT','DELETE'])
@login_required
def edit_achievement(aid):
    if request.method == 'DELETE':
        execute("DELETE FROM achievements WHERE id=%s", (aid,))
        return jsonify({'success': True})
    d = request.get_json()
    execute("UPDATE achievements SET title=%s,description=%s,icon=%s WHERE id=%s",
            (d['title'],d['description'],d.get('icon','🏆'),aid))
    return jsonify({'success': True})

# ─── Admin API — Certifications ───────────────────────────────────────────────
@app.route('/admin/api/certifications', methods=['POST'])
@login_required
def add_cert():
    d = request.get_json()
    execute("INSERT INTO certifications (name,issuer,year,url) VALUES (%s,%s,%s,%s)",
            (d['name'],d['issuer'],d.get('year',''),d.get('url','')))
    return jsonify({'success': True})

@app.route('/admin/api/certifications/<int:cid>', methods=['DELETE'])
@login_required
def delete_cert(cid):
    execute("DELETE FROM certifications WHERE id=%s", (cid,))
    return jsonify({'success': True})

# ─── Admin API — Password Change ──────────────────────────────────────────────
@app.route('/admin/api/change-password', methods=['POST'])
@login_required
def change_password():
    d = request.get_json()
    hashed = hashlib.sha256(d['new_password'].encode()).hexdigest()
    execute("UPDATE admin SET password_hash=%s WHERE id=1", (hashed,))
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)