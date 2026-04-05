# авторизация
class AuthorizationModule:
    def __init__(self, users_db):
        self.users_db = users_db
        self.current_login = None

    def authenticate(self, login, password):
        user = self.users_db.get_user_by_login(login)
        if user and user['password'] == password:
            self.current_login = login
            return dict(user)
        return None

    def register_user(self, fio, login, password, role):
        return self.users_db.add_user(fio, login, password, role)

    def logout(self):
        self.current_login = None

# разграничение прав доступа в систему
class AccessControlModule:
    def __init__(self, auth_module, users_db):
        self.auth_module = auth_module
        self.users_db = users_db

    def verify_access(self, required_role="Охранник"):
        if not self.auth_module.current_login:
            raise PermissionError("Пользователь не авторизован.")
        
        user = self.users_db.get_user_by_login(self.auth_module.current_login)
        if not user:
            raise PermissionError("Пользователь не найден в базе данных.")
            
        if required_role == "Диспетчер" and user['role'] != "Диспетчер":
            raise PermissionError("Отказано в доступе. Требуются права Диспетчера.")
        return True

# обработка объектов
class ObjectsProcessingModule:
    def __init__(self, access_control, objects_db):
        self.access_control = access_control
        self.objects_db = objects_db

    def get_list(self):
        self.access_control.verify_access(required_role="Диспетчер")
        return self.objects_db.get_all_objects()

    def add_new(self, name, address, obj_type, min_guards):
        self.access_control.verify_access(required_role="Диспетчер")
        self.objects_db.add_object(name, address, obj_type, min_guards)

    def remove(self, obj_id):
        self.access_control.verify_access(required_role="Диспетчер")
        if not self.objects_db.get_object_by_id(obj_id):
            raise ValueError(f"Объект с ID {obj_id} не найден в базе данных.")
        self.objects_db.delete_object(obj_id)

# обработка сотрудников
class GuardsProcessingModule:
    def __init__(self, access_control, guards_db):
        self.access_control = access_control
        self.guards_db = guards_db

    def get_list(self):
        self.access_control.verify_access(required_role="Диспетчер")
        return self.guards_db.get_all_guards()

    def add_new(self, fio, position, phone, status):
        self.access_control.verify_access(required_role="Диспетчер")
        self.guards_db.add_guard(fio, position, phone, status)

    def change_status(self, guard_id, status):
        self.access_control.verify_access(required_role="Диспетчер")
        if not self.guards_db.get_guard_by_id(guard_id):
            raise ValueError(f"Сотрудник охраны с ID {guard_id} не найден в базе данных.")
        self.guards_db.update_guard_status(guard_id, status)

    def remove(self, guard_id):
        self.access_control.verify_access(required_role="Диспетчер")
        if not self.guards_db.get_guard_by_id(guard_id):
            raise ValueError(f"Сотрудник охраны с ID {guard_id} не найден в базе данных.")
        self.guards_db.delete_guard(guard_id)

# обработка тревог
class IncidentsProcessingModule:
    def __init__(self, access_control, dal):
        self.access_control = access_control
        self.dal = dal

    def get_list(self):
        self.access_control.verify_access(required_role="Охранник")
        return self.dal.incidents.get_all_incidents()

    def report(self, object_id, guard_id, description, date, status):
        self.access_control.verify_access(required_role="Охранник")
        if not self.dal.objects.get_object_by_id(object_id):
            raise ValueError(f"Объект с ID {object_id} не найден в базе данных.")
        if not self.dal.guards.get_guard_by_id(guard_id):
            raise ValueError(f"Сотрудник охраны с ID {guard_id} не найден в базе данных.")
        self.dal.incidents.add_incident(object_id, guard_id, description, date, status)

    def change_status(self, incident_id, status):
        self.access_control.verify_access(required_role="Охранник")
        if not self.dal.incidents.get_incident_by_id(incident_id):
            raise ValueError(f"Тревога с ID {incident_id} не найдена в базе данных.")
        self.dal.incidents.update_incident_status(incident_id, status)

# слой бизнес-логики
class BusinessLogicLayer:
    def __init__(self, dal):
        self.auth = AuthorizationModule(dal.users)
        self.access = AccessControlModule(self.auth, dal.users)
        self.objects = ObjectsProcessingModule(self.access, dal.objects)
        self.guards = GuardsProcessingModule(self.access, dal.guards)
        self.incidents = IncidentsProcessingModule(self.access, dal)