from src.models import Order, Client, Furniture, load_data, save_data, ORDERS_FILE, CLIENTS_FILE

def get_next_id(data):
    if not data:
        return 1
    return max(item.get("id", 0) for item in data) + 1

def create_client():
    print("\n=== Добавление клиента ===")
    name = input("ФИО клиента: ")
    phone = input("Телефон: ")
    address = input("Адрес: ")
    
    clients = load_data(CLIENTS_FILE)
    client = Client(name, phone, address)
    client.id = get_next_id(clients)
    clients.append(client.to_dict())
    save_data(CLIENTS_FILE, clients)
    
    print(f"✅ Клиент добавлен! ID: {client.id}")
    return client.id

def create_order(designer_name):
    print("\n=== Создание нового заказа ===")
    
    # Выбор или создание клиента
    clients = load_data(CLIENTS_FILE)
    if clients:
        print("\nСуществующие клиенты:")
        for c in clients:
            print(f"  {c['id']}. {c['name']} - {c['phone']}")
    
    choice = input("\nВыбрать существующего клиента (1) или создать нового (2)? ")
    if choice == "1":
        client_id = int(input("Введите ID клиента: "))
    else:
        client_id = create_client()
    
    # Параметры мебели
    print("\n=== Параметры мебели ===")
    type_name = input("Тип мебели (Шкаф/Кухня/Стол/Тумба): ")
    length = float(input("Длина (см): "))
    width = float(input("Ширина (см): "))
    print("Материалы: ДСП, МДФ, Массив")
    material = input("Материал: ")
    
    furniture = Furniture(type_name, length, width, material)
    order = Order(client_id, furniture, designer_name)
    
    # Сохраняем заказ
    orders = load_data(ORDERS_FILE)
    order.id = get_next_id(orders)
    orders.append(order.to_dict())
    save_data(ORDERS_FILE, orders)
    
    prelim_price = order.calculate_preliminary_price()
    print(f"\n✅ Заказ #{order.id} создан!")
    print(f"   Предварительная стоимость: {prelim_price:,.0f} руб.")
    print(f"   Статус: {order.status}")
    
    return order.id

def list_orders():
    orders = load_data(ORDERS_FILE)
    clients = {c["id"]: c for c in load_data(CLIENTS_FILE)}
    
    if not orders:
        print("\nНет заказов")
        return
    
    print("\n" + "="*70)
    print(f"{'ID':<4} {'Клиент':<20} {'Статус':<18} {'Стоимость':<15} {'Остаток':<10}")
    print("-"*70)
    
    for order in orders:
        client = clients.get(order["client_id"], {})
        client_name = client.get("name", "Неизвестно")[:20]
        final = order.get("final_price") if order.get("final_price") else order.get("prelim_price", 0)
        remaining = final - order.get("prepayment", 0)
        print(f"{order['id']:<4} {client_name:<20} {order['status']:<18} {final:,.0f} руб.  {remaining:,.0f} руб.")
    print("="*70)

def get_order(order_id):
    orders = load_data(ORDERS_FILE)
    for order in orders:
        if order["id"] == order_id:
            return order
    return None

def update_status(order_id, new_status):
    orders = load_data(ORDERS_FILE)
    for order in orders:
        if order["id"] == order_id:
            order["status"] = new_status
            save_data(ORDERS_FILE, orders)
            print(f"✅ Статус заказа #{order_id} изменен на: {new_status}")
            return True
    print(f"❌ Заказ #{order_id} не найден")
    return False

def get_orders_by_status(status):
    orders = load_data(ORDERS_FILE)
    return [o for o in orders if o["status"] == status]
