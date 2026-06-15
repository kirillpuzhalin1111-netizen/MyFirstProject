from src.models import load_data, ORDERS_FILE
from datetime import datetime

def revenue_report():
    orders = load_data(ORDERS_FILE)
    
    print("\n" + "="*60)
    print("ОТЧЕТ ПО ВЫРУЧКЕ")
    print("="*60)
    
    total_revenue = 0
    total_prepayment = 0
    
    print(f"\n{'Заказ':<8} {'Статус':<18} {'Предоплата':<15} {'Итого':<15}")
    print("-"*56)
    
    for order in orders:
        prepayment = order.get("prepayment", 0)
        final = order.get("final_price", 0)
        total_prepayment += prepayment
        total_revenue += final
        
        status = order.get("status", "Новый")
        print(f"#{order['id']:<7} {status:<18} {prepayment:,.0f} руб.    {final:,.0f} руб.")
    
    print("-"*56)
    print(f"\n📊 Общая выручка: {total_revenue:,.0f} руб.")
    print(f"💰 Сумма предоплат: {total_prepayment:,.0f} руб.")
    print(f"📋 Всего заказов: {len(orders)}")
    
    # Налог (УСН 6%)
    tax = total_revenue * 0.06
    print(f"\n📝 Налог (УСН 6%): {tax:,.0f} руб.")
    print("="*60)

def active_orders_report():
    orders = load_data(ORDERS_FILE)
    active_statuses = ["Новый", "Замер", "Смета согласована", "Предоплата", "В производстве", "Готово"]
    active = [o for o in orders if o["status"] in active_statuses]
    
    print("\n" + "="*60)
    print("АКТИВНЫЕ ЗАКАЗЫ")
    print("="*60)
    
    if not active:
        print("Нет активных заказов")
        return
    
    for order in active:
        final = order.get("final_price", 0)
        prepayment = order.get("prepayment", 0)
        remaining = final - prepayment
        
        print(f"\nЗаказ #{order['id']}")
        print(f"  Статус: {order['status']}")
        print(f"  Стоимость: {final:,.0f} руб.")
        print(f"  Предоплата: {prepayment:,.0f} руб.")
        print(f"  Остаток: {remaining:,.0f} руб.")
