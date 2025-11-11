#!/usr/bin/env python3
"""
Verify database has data - used for deployment verification
"""
import sqlite3
from db import DB_PATH

def verify_database():
    """Verify database has data"""
    print("🔍 Verifying database data...")
    print(f"Database path: {DB_PATH}")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        # Check all tables
        tables = ['leagues', 'teams', 'players', 'matches', 'users']
        total_records = 0
        
        for table in tables:
            cur.execute(f'SELECT COUNT(*) FROM {table}')
            count = cur.fetchone()[0]
            total_records += count
            print(f"  {table.upper():15} : {count:6} records")
        
        conn.close()
        
        if total_records > 0:
            print(f"\n✅ Database verification PASSED! Total records: {total_records}")
            return True
        else:
            print(f"\n❌ Database verification FAILED! No data found.")
            return False
            
    except Exception as e:
        print(f"\n❌ Database verification ERROR: {str(e)}")
        return False

if __name__ == '__main__':
    verify_database()
