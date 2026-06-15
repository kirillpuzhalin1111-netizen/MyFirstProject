import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

ORDERS_FILE = "orders.json"
CLIENTS_FILE = "clients.json"

USERS = {
    "designer1": {"password": "123", "role": "designer", "name": "Анна Дизайнер"},
    "manager1": {"password": "123", "role": "manager", "name": "Иван Менеджер"},
    "accountant1": {"password": "123", "role": "accountant", "name": "Елена Бухгалтер"},
    "admin1": {"password": "123", "role": "admin", "name": "Админ"}
}

current_user = None

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

def get_next_id(data):
    if not data:
        return 1
    return max(item.get("id", 0) for item in data) + 1

def calculate_price(furniture_type, length, width, material):
    prices = {"ДСП": 5000, "МДФ": 8000, "Массив": 15000}
    base_price = prices.get(material, 5000)
    coeff = {"Шкаф": 1.0, "Кухня": 1.2, "Стол": 0.8, "Тумба": 0.9}
    type_coeff = coeff.get(furniture_type, 1.0)
    area = (float(length) * float(width)) / 10000
    return area * base_price * type_coeff

class LoginWindow:
    def __init__(self, root):
        self.root = root
        root.title("MebelFlow - Вход в систему")
        root.geometry("400x380")
        root.resizable(False, False)
        root.eval('tk::PlaceWindow . center')
        
        frame = tk.Frame(root, padx=40, pady=40)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="🏢 MebelFlow", font=("Arial", 20, "bold")).pack(pady=(0, 20))
        tk.Label(frame, text="Вход в систему", font=("Arial", 12)).pack(pady=(0, 30))
        
        tk.Label(frame, text="Логин:", font=("Arial", 10)).pack(anchor=tk.W)
        self.entry_login = tk.Entry(frame, font=("Arial", 11), width=30)
        self.entry_login.pack(fill=tk.X, pady=(5, 15))
        
        tk.Label(frame, text="Пароль:", font=("Arial", 10)).pack(anchor=tk.W)
        self.entry_password = tk.Entry(frame, font=("Arial", 11), width=30, show="*")
        self.entry_password.pack(fill=tk.X, pady=(5, 20))
        
        tk.Button(frame, text="Войти", font=("Arial", 11), bg="#4CAF50", fg="white",
                  command=self.login, width=20).pack()
        
        tk.Label(frame, text="Тестовые учетные записи:\ndesigner1 / 123\nmanager1 / 123", 
                 font=("Arial", 8), fg="gray").pack(pady=(20, 0))
        
        self.entry_password.bind("<Return>", lambda e: self.login())
        self.entry_login.focus()
    
    def login(self):
        global current_user
        username = self.entry_login.get()
        password = self.entry_password.get()
        
        if username in USERS and USERS[username]["password"] == password:
            current_user = USERS[username]
            self.root.destroy()
            root = tk.Tk()
            app = MainWindow(root)
            root.mainloop()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

class MainWindow:
    def __init__(self, root):
        self.root = root
        root.title(f"MebelFlow - {current_user['name']}")
        root.geometry("1000x600")
        
        toolbar = tk.Frame(root, bg="#f0f0f0", height=50)
        toolbar.pack(fill=tk.X, side=tk.TOP)
        
        role = current_user["role"]
        
        if role in ["designer", "manager", "admin"]:
            tk.Button(toolbar, text="➕ Новый заказ", command=self.new_order,
                     bg="#4CAF50", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5, pady=10)
        
        if role in ["manager", "admin"]:
            tk.Button(toolbar, text="💰 Предоплата", command=self.prepayment,
                     bg="#2196F3", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5, pady=10)
            tk.Button(toolbar, text="📊 Отчет", command=self.report,
                     bg="#FF9800", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5, pady=10)
        
        if role in ["accountant", "admin"]:
            tk.Button(toolbar, text="📈 Финансы", command=self.finance_report,
                     bg="#9C27B0", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5, pady=10)
        
        tk.Button(toolbar, text="🔄 Обновить", command=self.refresh_orders,
                 bg="#607D8B", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5, pady=10)
        
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scroll_y = tk.Scrollbar(frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        columns = ("ID", "Клиент", "Тип", "Размеры", "Материал", "Стоимость", "Предоплата", "Статус")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings",
                                  yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.column("Клиент", width=150)
        self.tree.column("Статус", width=120)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        self.tree.bind("<Double-1>", self.view_order)
        
        self.statusbar = tk.Label(root, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.refresh_orders()
    
    def refresh_orders(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        orders = load_data(ORDERS_FILE)
        clients = {c["id"]: c for c in load_data(CLIENTS_FILE)}
        
        for order in orders:
            client = clients.get(order["client_id"], {})
            client_name = client.get("name", "Неизвестно")[:20]
            furniture = order.get("furniture", {})
            dimensions = f"{furniture.get('length', '')}x{furniture.get('width', '')} см"
            final_price = order.get("final_price") or order.get("prelim_price", 0)
            
            self.tree.insert("", tk.END, values=(
                order.get("id", ""), client_name,
                furniture.get("type", ""), dimensions,
                furniture.get("material", ""),
                f"{final_price:,.0f}", f"{order.get('prepayment', 0):,.0f}",
                order.get("status", "Новый")
            ))
        
        self.statusbar.config(text=f"Всего заказов: {len(orders)}")
    
    def new_order(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Новый заказ")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.eval('tk::PlaceWindow . center')
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="ДАННЫЕ КЛИЕНТА", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0,10))
        
        tk.Label(frame, text="ФИО клиента:").pack(anchor=tk.W)
        entry_name = tk.Entry(frame, width=40)
        entry_name.pack(fill=tk.X, pady=(0,10))
        
        tk.Label(frame, text="Телефон:").pack(anchor=tk.W)
        entry_phone = tk.Entry(frame, width=40)
        entry_phone.pack(fill=tk.X, pady=(0,10))
        
        tk.Label(frame, text="Адрес:").pack(anchor=tk.W)
        entry_address = tk.Entry(frame, width=40)
        entry_address.pack(fill=tk.X, pady=(0,20))
        
        tk.Label(frame, text="ПАРАМЕТРЫ МЕБЕЛИ", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0,10))
        
        row1 = tk.Frame(frame)
        row1.pack(fill=tk.X, pady=5)
        tk.Label(row1, text="Тип мебели:", width=15).pack(side=tk.LEFT)
        combo_type = ttk.Combobox(row1, values=["Шкаф", "Кухня", "Стол", "Тумба"], width=25)
        combo_type.pack(side=tk.LEFT)
        
        row2 = tk.Frame(frame)
        row2.pack(fill=tk.X, pady=5)
        tk.Label(row2, text="Длина (см):", width=15).pack(side=tk.LEFT)
        entry_length = tk.Entry(row2, width=28)
        entry_length.pack(side=tk.LEFT)
        
        row3 = tk.Frame(frame)
        row3.pack(fill=tk.X, pady=5)
        tk.Label(row3, text="Ширина (см):", width=15).pack(side=tk.LEFT)
        entry_width = tk.Entry(row3, width=28)
        entry_width.pack(side=tk.LEFT)
        
        row4 = tk.Frame(frame)
        row4.pack(fill=tk.X, pady=5)
        tk.Label(row4, text="Материал:", width=15).pack(side=tk.LEFT)
        combo_material = ttk.Combobox(row4, values=["ДСП", "МДФ", "Массив"], width=25)
        combo_material.pack(side=tk.LEFT)
        
        price_label = tk.Label(frame, text="Предварительная стоимость: 0 руб.", font=("Arial", 12, "bold"), fg="green")
        price_label.pack(pady=20)
        
        def update_price(*args):
            try:
                length = float(entry_length.get()) if entry_length.get() else 0
                width = float(entry_width.get()) if entry_width.get() else 0
                if length > 0 and width > 0 and combo_type.get() and combo_material.get():
                    price = calculate_price(combo_type.get(), length, width, combo_material.get())
                    price_label.config(text=f"Предварительная стоимость: {price:,.0f} руб.")
            except:
                pass
        
        combo_type.bind("<<ComboboxSelected>>", update_price)
        combo_material.bind("<<ComboboxSelected>>", update_price)
        entry_length.bind("<KeyRelease>", update_price)
        entry_width.bind("<KeyRelease>", update_price)
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=20)
        
        def save_order():
            if not entry_name.get():
                messagebox.showerror("Ошибка", "Введите ФИО клиента")
                return
            
            clients = load_data(CLIENTS_FILE)
            client_id = get_next_id(clients)
            clients.append({"id": client_id, "name": entry_name.get(), "phone": entry_phone.get(), "address": entry_address.get()})
            save_data(CLIENTS_FILE, clients)
            
            orders = load_data(ORDERS_FILE)
            order_id = get_next_id(orders)
            price = calculate_price(combo_type.get(), float(entry_length.get()), float(entry_width.get()), combo_material.get())
            
            orders.append({
                "id": order_id, "client_id": client_id, "designer_name": current_user["name"],
                "furniture": {"type": combo_type.get(), "length": float(entry_length.get()), 
                              "width": float(entry_width.get()), "material": combo_material.get()},
                "status": "Новый", "prepayment": 0, "final_price": None, "actual_cost": None,
                "prelim_price": price, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_data(ORDERS_FILE, orders)
            messagebox.showinfo("Успех", f"Заказ #{order_id} создан!\nСтоимость: {price:,.0f} руб.")
            dialog.destroy()
            self.refresh_orders()
        
        tk.Button(btn_frame, text="Сохранить", bg="#4CAF50", fg="white", command=save_order, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def prepayment(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите заказ")
            return
        order_id = int(self.tree.item(selected[0])['values'][0])
        orders = load_data(ORDERS_FILE)
        for order in orders:
            if order["id"] == order_id:
                prelim = order.get("prelim_price", 0)
                amount = simpledialog.askfloat("Предоплата", f"Заказ #{order_id}\nСтоимость: {prelim:,.0f} руб.\nМин. предоплата (50%): {prelim*0.5:,.0f} руб.\n\nСумма:")
                if amount:
                    if amount < prelim * 0.5:
                        messagebox.showerror("Ошибка", f"Предоплата не может быть меньше {prelim*0.5:,.0f} руб.")
                        return
                    order["prepayment"] = amount
                    order["status"] = "В производстве" if amount >= prelim else "Предоплата"
                    save_data(ORDERS_FILE, orders)
                    messagebox.showinfo("Успех", f"Предоплата {amount:,.0f} руб. зарегистрирована")
                    self.refresh_orders()
                return
    
    def report(self):
        orders = load_data(ORDERS_FILE)
        total = sum(o.get("final_price") or o.get("prelim_price", 0) for o in orders)
        prepay = sum(o.get("prepayment", 0) for o in orders)
        messagebox.showinfo("Финансовый отчет", f"📊 ОТЧЕТ ПО ВЫРУЧКЕ\n{'='*40}\n\nВсего заказов: {len(orders)}\nОбщая выручка: {total:,.0f} руб.\nСумма предоплат: {prepay:,.0f} руб.\nНалог (УСН 6%): {total*0.06:,.0f} руб.")
    
    def finance_report(self):
        orders = load_data(ORDERS_FILE)
        active = [o for o in orders if o.get("status") not in ["Закрыт", "Доставка"]]
        messagebox.showinfo("Финансовый отчет", f"📈 ФИНАНСОВЫЙ ОТЧЕТ\n{'='*40}\n\nАктивных заказов: {len(active)}\nВсего заказов: {len(orders)}")
    
    def view_order(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        order_id = int(self.tree.item(selected[0])['values'][0])
        orders = load_data(ORDERS_FILE)
        clients = {c["id"]: c for c in load_data(CLIENTS_FILE)}
        for order in orders:
            if order["id"] == order_id:
                client = clients.get(order["client_id"], {})
                dialog = tk.Toplevel(self.root)
                dialog.title(f"Заказ #{order_id}")
                dialog.geometry("400x450")
                dialog.transient(self.root)
                dialog.grab_set()
                frame = tk.Frame(dialog, padx=20, pady=20)
                frame.pack(fill=tk.BOTH, expand=True)
                info = f"=== ЗАКАЗ #{order_id} ===\n\nСтатус: {order.get('status')}\n\n=== КЛИЕНТ ===\nФИО: {client.get('name')}\nТелефон: {client.get('phone')}\nАдрес: {client.get('address')}\n\n=== МЕБЕЛЬ ===\nТип: {order.get('furniture', {}).get('type')}\nРазмеры: {order.get('furniture', {}).get('length')}x{order.get('furniture', {}).get('width')} см\nМатериал: {order.get('furniture', {}).get('material')}\n\n=== ФИНАНСЫ ===\nСтоимость: {order.get('prelim_price', 0):,.0f} руб.\nПредоплата: {order.get('prepayment', 0):,.0f} руб.\nОстаток: {order.get('prelim_price', 0) - order.get('prepayment', 0):,.0f} руб."
                text = tk.Text(frame, height=18, width=50)
                text.pack(fill=tk.BOTH, expand=True)
                text.insert(tk.END, info)
                text.config(state=tk.DISABLED)
                tk.Button(frame, text="Закрыть", command=dialog.destroy).pack(pady=10)
                return
    
    def logout(self):
        if messagebox.askyesno("Выход", "Вы уверены?"):
            self.root.destroy()
            root = tk.Tk()
            LoginWindow(root)
            root.mainloop()

if __name__ == "__main__":
    if not os.path.exists(ORDERS_FILE):
        save_data(ORDERS_FILE, [])
    if not os.path.exists(CLIENTS_FILE):
        save_data(CLIENTS_FILE, [])
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
