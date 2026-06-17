import sqlite3

def init_database():
    # Creamos o conectamos con el archivo local de la base de datos
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    
    # Tabla de firmwares cargados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS firmwares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            version TEXT,
            uploaded_by TEXT
        )
    ''')
    
    # Insertamos un usuario administrador de prueba (password en texto plano para la fase vulnerable)
    try:
        cursor.execute("INSERT INTO usuarios (username, password, role) VALUES ('admin_ucab', 'UCAB_Secret_2026', 'admin')")
        conn.commit()
        print("[+] Base de datos inicializada y usuario administrador creado con éxito.")
    except sqlite3.IntegrityError:
        print("[!] El usuario administrador ya existe.")
        
    conn.close()

if __name__ == '__main__':
    init_database()