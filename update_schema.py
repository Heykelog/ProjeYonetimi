"""
Database schema update script
Run this when there are model changes: python update_schema.py
"""
import sqlite3
import os

# Database path
DB_PATH = 'instance/pentest.db'

def check_db_exists():
    return os.path.exists(DB_PATH)

def add_column_if_not_exists(conn, table, column, dtype):
    """Add a column to a table if it doesn't exist"""
    cursor = conn.cursor()
    # Check if the column exists in the table
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [info[1] for info in cursor.fetchall()]
    
    if column not in columns:
        print(f"Adding column {column} to {table} table...")
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {dtype}")
        conn.commit()
        return True
    else:
        print(f"Column {column} already exists in {table} table.")
        return False

def update_schema():
    """Update the database schema for new fields"""
    if not check_db_exists():
        print(f"Database not found at {DB_PATH}")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    
    # Add new project fields
    add_column_if_not_exists(conn, 'projects', 'tags', 'VARCHAR(200)')
    add_column_if_not_exists(conn, 'projects', 'is_backlog', 'BOOLEAN DEFAULT 0')
    add_column_if_not_exists(conn, 'projects', 'priority', 'INTEGER DEFAULT 0')
    
    # Make pentest_date nullable (for backlog projects)
    cursor = conn.cursor()
    try:
        # SQLite doesn't support directly changing column constraints, so we need to use a workaround
        # We'll create a temporary table with the new schema, copy data, drop the old table, and rename
        print("Updating 'pentest_date' to be nullable...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            manager VARCHAR(100) NOT NULL,
            pentest_date DATE,
            project_type VARCHAR(20) NOT NULL,
            mandays FLOAT NOT NULL DEFAULT 0,
            extra_mandays FLOAT DEFAULT 0,
            extra_mandays_reason TEXT,
            completed BOOLEAN DEFAULT 0,
            company_id INTEGER NOT NULL,
            tags VARCHAR(200),
            is_backlog BOOLEAN DEFAULT 0,
            priority INTEGER DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES companies (id)
        )
        """)
        
        # Copy data from old table to new table
        cursor.execute("""
        INSERT INTO projects_new 
        SELECT id, name, manager, pentest_date, project_type, mandays, extra_mandays, 
               extra_mandays_reason, completed, company_id, tags, is_backlog, priority
        FROM projects
        """)
        
        # Drop old table and rename new table
        cursor.execute("DROP TABLE projects")
        cursor.execute("ALTER TABLE projects_new RENAME TO projects")
        
        conn.commit()
        print("Schema update completed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error updating schema: {e}")
        return False
    finally:
        conn.close()
    
    return True

if __name__ == "__main__":
    if update_schema():
        print("Database schema updated successfully.")
    else:
        print("Failed to update database schema.") 