import json
import os
from datetime import datetime

# Файлы для хранения данных
ORDERS_FILE = "orders.json"
CLIENTS_FILE = "clients.json"

def load_data(filename, default=None):
    if default is None:
        default = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class Client:
    def __init__(self, name, phone, address):
        self.id = None
        self.name = name
        self.phone = phone
        self.address = address
    
    def to_dict(self):
        return {"id": self.id, "name": self.name, "phone": self.phone, "address": self.address}
    
    @staticmethod
    def from_dict(data):
        client = Client(data["name"], data["phone"], data["address"])
        client.id = data["id"]
        return client

class Furniture:
    def __init__(self, type_name, length, width, material):
        self.type_name = type_name  # Шкаф, Кухня, Стол и т.д.
        self.length = length  # длина в см
        self.width = width    # ширина в см
        self.material = material  # ДСП, МДФ, Массив
    
    def calculate_area(self):
        return (self.length * self.width) / 10000  # в кв.м
    
    def calculate_price(self):
        # Цены за кв.м
        prices = {"ДСП": 5000, "МДФ": 8000, "Массив": 15000}
        base_price = prices.get(self.material, 5000)
        
        # Коэффициент для типа мебели
        coeff = {"Шкаф": 1.0, "Кухня": 1.2, "Стол": 0.8, "Тумба": 0.9}
        type_coeff = coeff.get(self.type_name, 1.0)
        
        return self.calculate_area() * base_price * type_coeff

class Order:
    STATUSES = ["Новый", "Замер", "Смета согласована", "Предоплата", "В производстве", "Готово", "Доставка", "Закрыт"]
    
    def __init__(self, client_id, furniture, designer_name):
        self.id = None
        self.client_id = client_id
        self.furniture = furniture
        self.designer_name = designer_name
        self.status = "Новый"
        self.prepayment = 0
        self.final_price = None
        self.actual_cost = None
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def calculate_preliminary_price(self):
        return self.furniture.calculate_price()
    
    def get_remaining_debt(self):
        final = self.final_price if self.final_price else self.calculate_preliminary_price()
        return final - self.prepayment
    
    def can_deliver(self):
        return self.get_remaining_debt() <= 0
    
    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "furniture": {
                "type": self.furniture.type_name,
                "length": self.furniture.length,
                "width": self.furniture.width,
                "material": self.furniture.material
            },
            "designer_name": self.designer_name,
            "status": self.status,
            "prepayment": self.prepayment,
            "final_price": self.final_price,
            "actual_cost": self.actual_cost,
            "created_at": self.created_at
        }
