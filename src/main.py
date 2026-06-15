import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth import login, get_current_user, is_designer, is_manager, is_accountant, is_admin
from src.orders import create_order, list_orders, update_status, get_order, get_orders_by_status
from src.finance import register_prepayment, set_final_price, register_full_payment, check_debt_for_delivery
from src.reports import revenue_report, active_orders_report

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def designer_menu():
    while True:
        print("\n" + "="*50)
        print("👨‍🎨 МЕНЮ ДИЗАЙНЕРА")
        print("="*50)
        print("1. Создать новый заказ")
        print("2. Просмотреть все заказы")
        print("3. Изменить статус заказа")
        print("4. Зарегистрировать предоплату")
        print("5. Выйти")
        
        choice = input("\nВыберите действие: ")
        
        if choice == "1":
            create_order(get_current_user()["name"])
            input("\nНажмите Enter для продолжения...")
        elif choice == "2":
            list_orders()
            input("\nНажмите Enter для продолжения...")
        elif choice == "3":
            order_id = int(input("ID заказа: "))
            print("\nДоступные статусы: Новый, Замер, Смета согласована")
            new_status = input("Новый статус: ")
            update_status(order_id, new_status)
            input("\nНажмите Enter для продолжения...")
        elif choice == "4":
            order_id = int(input("ID заказа: "))
            register_prepayment(order_id)
            input("\nНажмите Enter для продолжения...")
        elif choice == "5":
            break
        else:
            print("Неверный выбор")

def manager_menu():
    while True:
        print("\n" + "="*50)
        print("📋 МЕНЮ МЕНЕДЖЕРА")
        print("="*50)
        print("1. Просмотреть все заказы")
        print("2. Зарегистрировать предоплату")
        print("3. Установить окончательную стоимость")
        print("4. Принять полную оплату")
        print("5. Подтвердить доставку")
        print("6. Сформировать отчет по выручке")
        print("7. Выйти")
        
        choice = input("\nВыберите действие: ")
        
        if choice == "1":
            list_orders()
            input("\nНажмите Enter для продолжения...")
        elif choice == "2":
            order_id = int(input("ID заказа: "))
            register_prepayment(order_id)
            input("\nНажмите Enter для продолжения...")
        elif choice == "3":
            order_id = int(input("ID заказа: "))
            set_final_price(order_id)
            input("\nНажмите Enter для продолжения...")
        elif choice == "4":
            order_id = int(input("ID заказа: "))
            register_full_payment(order_id)
            input("\nНажмите Enter для продолжения...")
        elif choice == "5":
            order_id = int(input("ID заказа: "))
            if check_debt_for_delivery(order_id):
                update_status(order_id, "Доставка")
            input("\nНажмите Enter для продолжения...")
        elif choice == "6":
            revenue_report()
            input("\nНажмите Enter для продолжения...")
        elif choice == "7":
            break
        else:
            print("Неверный выбор")

def accountant_menu():
    while True:
        print("\n" + "="*50)
        print("💰 МЕНЮ БУХГАЛТЕРА")
        print("="*50)
        print("1. Отчет по выручке")
        print("2. Активные заказы")
        print("3. Просмотреть все заказы")
        print("4. Выйти")
        
        choice = input("\nВыберите действие: ")
        
        if choice == "1":
            revenue_report()
            input("\nНажмите Enter для продолжения...")
        elif choice == "2":
            active_orders_report()
            input("\nНажмите Enter для продолжения...")
        elif choice == "3":
            list_orders()
            input("\nНажмите Enter для продолжения...")
        elif choice == "4":
            break
        else:
            print("Неверный выбор")

def admin_menu():
    while True:
        print("\n" + "="*50)
        print("🔧 МЕНЮ АДМИНИСТРАТОРА")
        print("="*50)
        print("1. Просмотреть все заказы")
        print("2. Все отчеты")
        print("3. Выйти")
        
        choice = input("\nВыберите действие: ")
        
        if choice == "1":
            list_orders()
            input("\nНажмите Enter для продолжения...")
        elif choice == "2":
            revenue_report()
            active_orders_report()
            input("\nНажмите Enter для продолжения...")
        elif choice == "3":
            break
        else:
            print("Неверный выбор")

def main():
    clear_screen()
    print("\n" + "="*50)
    print("🏢 ДОБРО ПОЖАЛОВАТЬ В MebelFlow")
    print("="*50)
    
    if not login():
        return
    
    user = get_current_user()
    role = user["role"]
    
    if role == "designer":
        designer_menu()
    elif role == "manager":
        manager_menu()
    elif role == "accountant":
        accountant_menu()
    elif role == "admin":
        admin_menu()
    
    print("\n👋 До свидания!")

if __name__ == "__main__":
    main()
