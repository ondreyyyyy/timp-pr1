import sqlite3

# бд пользователей
class UsersDatabase:
    def __init__(self):
        self.db_file = 'users.db'
        self._initialize_table()

    def _initialize_table(self):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY, fio TEXT, login TEXT UNIQUE, password TEXT, role TEXT)''')

    def get_user_by_login(self, login):
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM users WHERE login = ?", (login,))
            return cursor.fetchone()

    def add_user(self, fio, login, password, role):
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute("INSERT INTO users (fio, login, password, role) VALUES (?, ?, ?, ?)", 
                             (fio, login, password, role))
            return True
        except sqlite3.IntegrityError:
            return False

# бд объектов
class ObjectsDatabase:
    def __init__(self):
        self.db_file = 'objects.db'
        self._initialize_table()

    def _initialize_table(self):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS objects 
                            (id INTEGER PRIMARY KEY, name TEXT, address TEXT, type TEXT, min_guards INTEGER)''')

    def get_all_objects(self):
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM objects").fetchall()

    def get_object_by_id(self, obj_id):
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM objects WHERE id = ?", (obj_id,)).fetchone()

    def add_object(self, name, address, obj_type, min_guards):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("INSERT INTO objects (name, address, type, min_guards) VALUES (?, ?, ?, ?)", 
                         (name, address, obj_type, min_guards))

    def delete_object(self, obj_id):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("DELETE FROM objects WHERE id = ?", (obj_id,))

# бд охраны
class GuardsDatabase:
    def __init__(self):
        self.db_file = 'guards.db'
        self._initialize_table()

    def _initialize_table(self):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS guards 
                            (id INTEGER PRIMARY KEY, fio TEXT, position TEXT, phone TEXT, status TEXT)''')

    def get_all_guards(self):
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM guards").fetchall()

    def get_guard_by_id(self, guard_id):
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM guards WHERE id = ?", (guard_id,)).fetchone()

    def add_guard(self, fio, position, phone, status):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("INSERT INTO guards (fio, position, phone, status) VALUES (?, ?, ?, ?)", 
                         (fio, position, phone, status))

    def update_guard_status(self, guard_id, new_status):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("UPDATE guards SET status = ? WHERE id = ?", (new_status, guard_id))

    def delete_guard(self, guard_id):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("DELETE FROM guards WHERE id = ?", (guard_id,))

# бд тревог
class IncidentsDatabase:
    def __init__(self):
        self.db_file = 'incidents.db'
        self._initialize_table()

    def _initialize_table(self):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS incidents 
                            (id INTEGER PRIMARY KEY, object_id INTEGER, guard_id INTEGER, description TEXT, date TEXT, status TEXT)''')

    def get_all_incidents(self):
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM incidents").fetchall()

    def get_incident_by_id(self, incident_id):
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()

    def add_incident(self, object_id, guard_id, description, date, status):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("INSERT INTO incidents (object_id, guard_id, description, date, status) VALUES (?, ?, ?, ?, ?)", 
                         (object_id, guard_id, description, date, status))

    def update_incident_status(self, incident_id, new_status):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("UPDATE incidents SET status = ? WHERE id = ?", (new_status, incident_id))

# слой доступа к данным
class DataAccessLayer:
    def __init__(self):
        self.users = UsersDatabase()
        self.objects = ObjectsDatabase()
        self.guards = GuardsDatabase()
        self.incidents = IncidentsDatabase()