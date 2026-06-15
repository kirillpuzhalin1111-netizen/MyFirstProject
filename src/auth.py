# Роли пользователей
ROLES = {
    "designer": "Дизайнер",
    "manager": "Менеджер", 
    "accountant": "Бухгалтер",
    "admin": "Администратор"
}

# База пользователей (логин: пароль, роль)
USERS = {
    "designer1": {"password": "123", "role": "designer", "name": "Анна Дизайнер"},
    "manager1": {"password": "123", "role": "manager", "name": "Иван Менеджер"},
    "accountant1": {"password": "123", "role": "accountant", "name": "Елена Бухгалтер"},
    "admin1": {"password": "123", "role": "admin", "name": "Админ"}
}

current_user = None

def login():
    global current_user
    print("\n=== Авторизация в MebelFlow ===")
    username = input("Логин: ")
    password = input("Пароль: ")
    
    if username in USERS and USERS[username]["password"] == password:
        current_user = USERS[username]
        print(f"\n✅ Добро пожаловать, {current_user['name']}!")
        print(f"   Роль: {ROLES[current_user['role']]}")
        return True
    else:
        print("\n❌ Неверный логин или пароль")
        return False

def get_current_user():
    return current_user

def has_role(role):
    return current_user and current_user["role"] == role

def is_designer():
    return has_role("designer")

def is_manager():
    return has_role("manager")

def is_accountant():
    return has_role("accountant")

def is_admin():
    return has_role("admin")
