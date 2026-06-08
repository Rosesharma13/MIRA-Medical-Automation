import sqlite3
from datetime import datetime

DB_PATH = "mira_patients.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            glucose REAL NOT NULL,
            haemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            remarks TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def create_patient(full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks=""):
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO patients (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (full_name, date_of_birth, email, float(glucose), float(haemoglobin), float(cholesterol), remarks))
        conn.commit()
        return True, "Patient record created successfully."
    except sqlite3.IntegrityError:
        return False, "A patient with this email already exists."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def read_all_patients():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM patients ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def read_patient_by_id(patient_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_patient(patient_id, full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks=""):
    conn = get_connection()
    try:
        conn.execute("""
            UPDATE patients
            SET full_name=?, date_of_birth=?, email=?, glucose=?, haemoglobin=?, cholesterol=?, remarks=?, updated_at=?
            WHERE id=?
        """, (full_name, date_of_birth, email, float(glucose), float(haemoglobin), float(cholesterol), remarks,
              datetime.now().strftime("%Y-%m-%d %H:%M:%S"), patient_id))
        conn.commit()
        return True, "Patient record updated successfully."
    except sqlite3.IntegrityError:
        return False, "Another patient with this email already exists."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_patient(patient_id):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        conn.commit()
        return True, "Patient record deleted successfully."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def search_patients(query):
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM patients
        WHERE full_name LIKE ? OR email LIKE ?
        ORDER BY created_at DESC
    """, (f"%{query}%", f"%{query}%")).fetchall()
    conn.close()
    return [dict(r) for r in rows]
