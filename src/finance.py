from src.models import load_data, save_data, ORDERS_FILE, CLIENTS_FILE

def register_prepayment(order_id):
    orders = load_data(ORDERS_FILE)
    for order in orders:
        if order["id"] == order_id:
            prelim = order.get("final_price") if order.get("final_price") else 0
            if prelim == 0:
                # Если финальной цены нет, используем предварительную
                from src.orders import get_order
                temp = get_order(order_id)
                if temp:
                    # Временно: нужно пересчитать
                    prelim = 50000  # Заглушка
            
            min_prepayment = prelim * 0.5  # 50% минимум
            print(f"\nЗаказ #{order_id}")
            print(f"Предварительная стоимость: {prelim:,.0f} руб.")
            print(f"Минимальная предоплата (50%): {min_prepayment:,.0f} руб.")
            
            amount = float(input("Сумма предоплаты: "))
            if amount < min_prepayment:
                print(f"❌ Предоплата не может быть меньше {min_prepayment:,.0f} руб.")
                return False
            
            order["prepayment"] = amount
            if amount >= prelim:
                order["status"] = "В производстве"
            else:
                order["status"] = "Предоплата"
            
            save_data(ORDERS_FILE, orders)
            print(f"✅ Предоплата {amount:,.0f} руб. зарегистрирована")
            print(f"   Остаток: {prelim - amount:,.0f} руб.")
            return True
    
    print(f"❌ Заказ #{order_id} не найден")
    return False

def set_final_price(order_id):
    orders = load_data(ORDERS_FILE)
    for order in orders:
        if order["id"] == order_id:
            print(f"\nЗаказ #{order_id}")
            print(f"Текущая предоплата: {order.get('prepayment', 0):,.0f} руб.")
            
            final = float(input("Введите окончательную стоимость: "))
            order["final_price"] = final
            order["status"] = "Готово"
            
            remaining = final - order.get("prepayment", 0)
            save_data(ORDERS_FILE, orders)
            print(f"✅ Окончательная стоимость: {final:,.0f} руб.")
            print(f"   Остаток к оплате: {remaining:,.0f} руб.")
            return True
    
    print(f"❌ Заказ #{order_id} не найден")
    return False

def register_full_payment(order_id):
    orders = load_data(ORDERS_FILE)
    for order in orders:
        if order["id"] == order_id:
            final = order.get("final_price")
            if not final:
                print("❌ Сначала установите окончательную стоимость")
                return False
            
            prepayment = order.get("prepayment", 0)
            remaining = final - prepayment
            
            if remaining <= 0:
                print("✅ Заказ уже полностью оплачен!")
                return True
            
            print(f"Остаток к оплате: {remaining:,.0f} руб.")
            confirm = input("Принять оплату? (да/нет): ")
            if confirm.lower() == "да":
                order["prepayment"] = final
                order["status"] = "Закрыт"
                save_data(ORDERS_FILE, orders)
                print(f"✅ Оплата принята! Заказ #{order_id} закрыт")
                return True
            return False
    
    print(f"❌ Заказ #{order_id} не найден")
    return False

def check_debt_for_delivery(order_id):
    orders = load_data(ORDERS_FILE)
    for order in orders:
        if order["id"] == order_id:
            final = order.get("final_price", 0)
            prepayment = order.get("prepayment", 0)
            remaining = final - prepayment
            
            if remaining > 0:
                print(f"❌ Невозможно отправить в доставку!")
                print(f"   Остаток долга: {remaining:,.0f} руб.")
                print(f"   Требуется полная оплата")
                return False
            return True
    return False
