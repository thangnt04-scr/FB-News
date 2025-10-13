#!/usr/bin/env python3
"""Fix admin password hash to use werkzeug hashing"""

import sqlite3
from werkzeug.security import generate_password_hash

# Connect to database
conn = sqlite3.connect('footballinfor.db')
cur = conn.cursor()

# Generate proper password hash
password_hash = generate_password_hash('admin123')

# Update admin user
cur.execute('UPDATE users SET password_hash = ? WHERE username = ?', (password_hash, 'admin'))
conn.commit()

print('✅ Updated admin password hash')

# Verify
cur.execute('SELECT username, email, role FROM users WHERE username = "admin"')
user = cur.fetchone()
if user:
    print(f'Admin user: {user[0]} ({user[1]}) - Role: {user[2]}')
else:
    print('❌ Admin user not found')

conn.close()

