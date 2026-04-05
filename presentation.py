import re
from datetime import datetime

# вход
class LoginUI:
    def __init__(self, auth_bl):
        self.auth_bl = auth_bl

    def do_login(self):
        while True:
            login = input("Логин: ").strip()
            if re.match(r"^[A-Za-z0-9_]{3,20}$", login): break
            print("Ошибка: Логин должен содержать от 3 до 20 символов (латиница, цифры, '_').")
            
        while True:
            password = input("Пароль: ").strip()
            if re.match(r"^[A-Za-z0-9!@#$%^&*()_\-+=\[\]{}|\\:;\"'<>,.?/]{4,50}$", password): break
            print("Ошибка: Пароль должен быть от 4 символов, без пробелов и кириллицы.")
        
        user = self.auth_bl.authenticate(login, password)
        if user:
            print(f"\n[УСПЕХ] Добро пожаловать, {user['fio']}!")
        else:
            print("[ОШИБКА] Неверный логин или пароль.")

# регистрация
class RegistrationUI:
    def __init__(self, auth_bl):
        self.auth_bl = auth_bl

    def do_register(self):
        print("\n--- РЕГИСТРАЦИЯ ---")
        while True:
            fio = input("ФИО: ").strip()
            if re.match(r"^[A-Za-zА-Яа-яЁё]+(?:[-\s][A-Za-zА-Яа-яЁё]+)+$", fio) and len(fio) >= 5:
                fio = fio.title()
                break
            print("Ошибка: Введите полное ФИО (минимум Имя и Фамилия), используя только буквы.")

        while True:
            login = input("Логин: ").strip()
            if re.match(r"^[A-Za-z0-9_]{3,20}$", login): break
            print("Ошибка: Логин должен содержать от 3 до 20 символов (латиница, цифры, '_').")

        while True:
            password = input("Пароль: ").strip()
            if re.match(r"^[A-Za-z0-9!@#$%^&*()_\-+=\[\]{}|\\:;\"'<>,.?/]{4,50}$", password): break
            print("Ошибка: Пароль должен быть от 4 символов, без пробелов и кириллицы.")

        while True:
            role = input("Роль (Охранник/Диспетчер): ").strip()
            if role.lower() in ['охранник', 'диспетчер']:
                role = 'Охранник' if role.lower() == 'охранник' else 'Диспетчер'
                break
            print("Ошибка: Пожалуйста, введите 'Охранник' или 'Диспетчер'.")
            
        success = self.auth_bl.register_user(fio, login, password, role)
        if success:
            user = self.auth_bl.authenticate(login, password)
            print(f"[УСПЕХ] Регистрация завершена! Добро пожаловать, {user['fio']}!")
        else:
            print("[ОШИБКА] Пользователь с таким логином уже существует.")

# отображение, добавление и удаление охраняемых объектов
class ObjectsUI:
    def __init__(self, objects_bl):
        self.objects_bl = objects_bl

    def objects_menu(self):
        print("\n--- ОХРАНЯЕМЫЕ ОБЪЕКТЫ ---")
        print("1. Показать все объекты\n2. Добавить объект\n3. Удалить объект\n0. Назад")
        act = input("Действие: ")
        
        try:
            if act == '1':
                objs = self.objects_bl.get_list()
                if not objs: print("Список объектов пуст.")
                else:
                    print("\nСписок объектов:")
                    for o in objs: print(f"[{o['id']}] Объект: {o['name']} (Тип: {o['type']}) | Адрес: {o['address']} | Мин. охрана: {o['min_guards']} чел.")
            
            elif act == '2':
                while True:
                    n = input("Название объекта: ").strip()
                    if n: break
                    print("Ошибка: Название не может быть пустым.")
                
                while True:
                    a = input("Адрес: ").strip()
                    if a: break
                    print("Ошибка: Адрес не может быть пустым.")
                
                while True:
                    t = input("Тип объекта (Склад/Офис/Магазин/Иное): ").strip()
                    types = {'склад': 'Склад', 'офис': 'Офис', 'магазин': 'Магазин', 'иное': 'Иное'}
                    if t.lower() in types:
                        t = types[t.lower()]
                        break
                    print("Ошибка: Выберите из предложенных вариантов.")
                
                while True:
                    m = input("Мин. количество охраны: ").strip()
                    if m.isdigit() and int(m) > 0:
                        m = int(m)
                        break
                    print("Ошибка: Введите положительное число.")
                
                self.objects_bl.add_new(n, a, t, m)
                print("[УСПЕХ] Объект успешно добавлен.")
            
            elif act == '3':
                while True:
                    i = input("ID объекта для удаления: ").strip()
                    if i.isdigit() and int(i) > 0:
                        i = int(i)
                        break
                    print("Ошибка: Введите корректный ID (число).")
                
                self.objects_bl.remove(i)
                print("[УСПЕХ] Команда на удаление выполнена.")
                
        except PermissionError as e:
            print(f"[СИСТЕМНАЯ ОШИБКА ДОСТУПА] {e}")
        except ValueError as e:
            print(f"[ОШИБКА ДАННЫХ] {e}")

# отображение, добавление и удаление сотрудников охраны, изменение текущего статуса
class GuardsUI:
    def __init__(self, guards_bl):
        self.guards_bl = guards_bl

    def guards_menu(self):
        print("\n--- СОТРУДНИКИ ОХРАНЫ ---")
        print("1. Показать сотрудников\n2. Добавить сотрудника\n3. Изменить статус\n4. Удалить\n0. Назад")
        act = input("Действие: ")
        
        try:
            if act == '1':
                guards = self.guards_bl.get_list()
                if not guards: print("Список сотрудников пуст.")
                else:
                    print("\nПерсонал:")
                    for g in guards: print(f"[{g['id']}] ФИО: {g['fio']} | Должность: {g['position']} | Тел: {g['phone']} | Статус: {g['status']}")
            
            elif act == '2':
                while True:
                    fio = input("ФИО сотрудника: ").strip()
                    if re.match(r"^[A-Za-zА-Яа-яЁё]+(?:[-\s][A-Za-zА-Яа-яЁё]+)+$", fio) and len(fio) >= 5:
                        fio = fio.title()
                        break
                    print("Ошибка: Введите полное ФИО (только буквы).")
                
                while True:
                    pos = input("Должность: ").strip()
                    if pos: break
                    print("Ошибка: Должность не может быть пустой.")
                
                while True:
                    phone = input("Номер телефона: ").strip()
                    clean_val = re.sub(r"[\s\-\(\)]", "", phone)
                    if re.match(r"^(?:\+7|8)[0-9]{10}$", clean_val):
                        phone = clean_val
                        break
                    print("Ошибка: Введите корректный номер телефона (+7... или 8...).")
                
                while True:
                    status = input("Статус (Свободен/На выезде/Не на смене): ").strip()
                    statuses = {'свободен': 'Свободен', 'на выезде': 'На выезде', 'не на смене': 'Не на смене'}
                    if status.lower() in statuses:
                        status = statuses[status.lower()]
                        break
                    print("Ошибка: Выберите один из предложенных статусов.")
                
                self.guards_bl.add_new(fio, pos, phone, status)
                print("[УСПЕХ] Сотрудник охраны добавлен.")
            
            elif act == '3':
                while True:
                    i = input("ID сотрудника: ").strip()
                    if i.isdigit() and int(i) > 0:
                        i = int(i)
                        break
                    print("Ошибка: Введите корректный ID (число).")
                
                while True:
                    new_status = input("Новый статус (Свободен/На выезде/Не на смене): ").strip()
                    statuses = {'свободен': 'Свободен', 'на выезде': 'На выезде', 'не на смене': 'Не на смене'}
                    if new_status.lower() in statuses:
                        new_status = statuses[new_status.lower()]
                        break
                    print("Ошибка: Выберите один из предложенных статусов.")
                
                self.guards_bl.change_status(i, new_status)
                print("[УСПЕХ] Статус сотрудника обновлен.")
            
            elif act == '4':
                while True:
                    i = input("ID сотрудника для удаления: ").strip()
                    if i.isdigit() and int(i) > 0:
                        i = int(i)
                        break
                    print("Ошибка: Введите корректный ID (число).")
                
                self.guards_bl.remove(i)
                print("[УСПЕХ] Сотрудник удален.")
                
        except PermissionError as e:
            print(f"[СИСТЕМНАЯ ОШИБКА ДОСТУПА] {e}")
        except ValueError as e:
            print(f"[ОШИБКА ДАННЫХ] {e}")

# отображение, объявление и изменение статуса тревог
class IncidentsUI:
    def __init__(self, incidents_bl):
        self.incidents_bl = incidents_bl

    def incidents_menu(self):
        print("\n--- ТРЕВОГИ (ИНЦИДЕНТЫ) ---")
        print("1. Показать тревоги\n2. Добавить (объявить) тревогу\n3. Изменить статус тревоги\n0. Назад")
        act = input("Действие: ")
        
        try:
            if act == '1':
                incidents = self.incidents_bl.get_list()
                if not incidents: print("Журнал тревог пуст.")
                else:
                    print("\nЖурнал инцидентов:")
                    for inc in incidents: print(f"[{inc['id']}] Дата: {inc['date']} | Объект ID: {inc['object_id']} | Охранник ID: {inc['guard_id']} | Статус: {inc['status']}\n    Описание: {inc['description']}")
            
            elif act == '2':
                while True:
                    obj_id = input("ID Объекта: ").strip()
                    if obj_id.isdigit() and int(obj_id) > 0:
                        obj_id = int(obj_id)
                        break
                    print("Ошибка: Введите корректный ID (число).")
                
                while True:
                    guard_id = input("ID Отправленного сотрудника: ").strip()
                    if guard_id.isdigit() and int(guard_id) > 0:
                        guard_id = int(guard_id)
                        break
                    print("Ошибка: Введите корректный ID (число).")
                
                while True:
                    desc = input("Описание происшествия: ").strip()
                    if desc: break
                    print("Ошибка: Описание не может быть пустым.")
                
                while True:
                    date = input("Дата происшествия (DD-MM-YYYY): ").strip()
                    try:
                        valid_date = datetime.strptime(date, "%d-%m-%Y")
                        date = valid_date.strftime("%d-%m-%Y")
                        break
                    except ValueError:
                        print("Ошибка: Некорректная дата. Введите в формате DD-MM-YYYY.")
                
                while True:
                    status = input("Статус (Активна/Решена/Ложная): ").strip()
                    statuses = {'активна': 'Активна', 'решена': 'Решена', 'ложная': 'Ложная'}
                    if status.lower() in statuses:
                        status = statuses[status.lower()]
                        break
                    print("Ошибка: Выберите один из предложенных статусов.")
                
                self.incidents_bl.report(obj_id, guard_id, desc, date, status)
                print("[УСПЕХ] Тревога зафиксирована в журнале.")
            
            elif act == '3':
                while True:
                    i = input("ID тревоги: ").strip()
                    if i.isdigit() and int(i) > 0:
                        i = int(i)
                        break
                    print("Ошибка: Введите корректный ID (число).")
                
                while True:
                    new_status = input("Новый статус (Активна/Решена/Ложная): ").strip()
                    statuses = {'активна': 'Активна', 'решена': 'Решена', 'ложная': 'Ложная'}
                    if new_status.lower() in statuses:
                        new_status = statuses[new_status.lower()]
                        break
                    print("Ошибка: Выберите один из предложенных статусов.")
                
                self.incidents_bl.change_status(i, new_status)
                print("[УСПЕХ] Статус тревоги изменен.")
                
        except PermissionError as e:
            print(f"[СИСТЕМНАЯ ОШИБКА ДОСТУПА] {e}")
        except ValueError as e:
            print(f"[ОШИБКА ДАННЫХ] {e}")

# слой представления
class PresentationLayer:
    def __init__(self, bl):
        self.bl = bl
        self.login_ui = LoginUI(bl.auth)
        self.register_ui = RegistrationUI(bl.auth)
        self.objects_ui = ObjectsUI(bl.objects)
        self.guards_ui = GuardsUI(bl.guards)
        self.incidents_ui = IncidentsUI(bl.incidents)

    def run(self):
        while True:
            if not self.bl.auth.current_login:
                self.auth_menu()
            else:
                self.system_menu()

    def auth_menu(self):
        print("\n=== СИСТЕМА БЕЗОПАСНОСТИ ===")
        print("1. Вход")
        print("2. Регистрация")
        print("3. Выход")
        choice = input("Выберите действие: ")

        if choice == '1': self.login_ui.do_login()
        elif choice == '2': self.register_ui.do_register()
        elif choice == '3': exit()

    def system_menu(self):
        print("\n--- ГЛАВНОЕ МЕНЮ ---")
        print("1. Управление объектами")
        print("2. Управление сотрудниками охраны")
        print("3. Управление тревогами")
        print("4. Выйти из аккаунта")
        
        choice = input("Действие: ")
        if choice == '1': self.objects_ui.objects_menu()
        elif choice == '2': self.guards_ui.guards_menu()
        elif choice == '3': self.incidents_ui.incidents_menu()
        elif choice == '4': self.bl.auth.logout()