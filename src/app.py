import datetime

def show_menu():
    print("\n=== Главное меню ===")
    print("1. Показать приветствие")
    print("2. Показать текущее время")
    print("3. Выйти")

def main():
    while True:
        show_menu()
        choice = input("Выберите действие (1-3): ")
        
        if choice == '1':
            name = input("Как вас зовут? ")
            print(f"Привет, {name}! Добро пожаловать в проект.")
        elif choice == '2':
            now = datetime.datetime.now()
            print(f"Текущее время: {now.strftime('%H:%M:%S')}")
        elif choice == '3':
            print("До свидания!")
            break
        else:
            print("Ошибка: выберите 1, 2 или 3.")

if __name__ == "__main__":
    main()
