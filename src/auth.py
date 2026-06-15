VALID_USER = "admin"
VALID_PASS = "1234"

def login():
    print("=== Система авторизации ===")
    username = input("Логин: ")
    password = input("Пароль: ")
    
    if username == VALID_USER and password == VALID_PASS:
        print("✅ Авторизация успешна!")
        return True
    else:
        print("❌ Неверный логин или пароль")
        return False
