import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# Название файла для хранения данных
DATA_FILE = 'expenses.json'

# Функция для загрузки данных из JSON
def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    return data

# Функция для сохранения данных в JSON
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Добавление расхода
def add_expense():
    amount_text = entry_amount.get()
    category = combo_category.get()
    date_text = entry_date.get()

    # Проверка суммы
    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Введите положительное число для суммы.")
        return

    # Проверка даты
    try:
        date_obj = datetime.strptime(date_text, '%Y-%m-%d')
        date_str = date_obj.strftime('%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД.")
        return

    # Добавление записи
    expense = {
        'amount': amount,
        'category': category,
        'date': date_str
    }

    data = load_data()
    data.append(expense)
    save_data(data)
    refresh_expenses()
    clear_inputs()

# Очистка полей
def clear_inputs():
    entry_amount.delete(0, tk.END)
    combo_category.set('')
    entry_date.delete(0, tk.END)
    entry_date.insert(0, datetime.now().strftime('%Y-%m-%d'))

# Обновление таблицы с расходами
def refresh_expenses(filtered_data=None):
    # Очистить таблицу
    for row in tree.get_children():
        tree.delete(row)

    data = filtered_data if filtered_data is not None else load_data()

    total = 0
    for expense in data:
        tree.insert('', tk.END, values=(expense['amount'], expense['category'], expense['date']))
        total += expense['amount']

    label_total.config(text=f"Общая сумма: {total:.2f}")

# Фильтрация по категории и дате
def filter_expenses():
    category_filter = combo_filter_category.get()
    start_date = entry_start_date.get()
    end_date = entry_end_date.get()

    data = load_data()
    filtered = []

    # Обработка дат
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_dt = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте формат дат (ГГГГ-ММ-ДД).")
        return

    for expense in data:
        date_obj = datetime.strptime(expense['date'], '%Y-%m-%d')
        # Фильтр по категории
        if category_filter != 'Все' and expense['category'] != category_filter:
            continue
        # Фильтр по дате
        if start_dt and date_obj < start_dt:
            continue
        if end_dt and date_obj > end_dt:
            continue
        filtered.append(expense)

    refresh_expenses(filtered)

# Создаем интерфейс
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x600")

# Ввод расходов
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
entry_amount = tk.Entry(frame_input)
entry_amount.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Категория:").grid(row=0, column=2, padx=5, pady=5)
categories = ['Еда', 'Транспорт', 'Развлечения', 'Общее']
combo_category = ttk.Combobox(frame_input, values=categories, state='readonly')
combo_category.grid(row=0, column=3, padx=5, pady=5)
combo_category.set(categories[0])

tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4, padx=5, pady=5)
entry_date = tk.Entry(frame_input)
entry_date.grid(row=0, column=5, padx=5, pady=5)
entry_date.insert(0, datetime.now().strftime('%Y-%m-%d'))

btn_add = tk.Button(frame_input, text="Добавить расход", command=add_expense)
btn_add.grid(row=0, column=6, padx=5, pady=5)

# Таблица расходов
columns = ('Сумма', 'Категория', 'Дата')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill='both', expand=True, padx=10, pady=10)

# Общая сумма
label_total = tk.Label(root, text="Общая сумма: 0.00", font=('Arial', 14))
label_total.pack()

# Фильтры
frame_filter = tk.Frame(root)
frame_filter.pack(pady=10)

# Категория фильтра
tk.Label(frame_filter, text="Фильтр по категории:").grid(row=0, column=0, padx=5)
combo_filter_category = ttk.Combobox(frame_filter, values=['Все'] + categories, state='readonly')
combo_filter_category.grid(row=0, column=1, padx=5)
combo_filter_category.set('Все')

# Дата фильтра
tk.Label(frame_filter, text="От:").grid(row=0, column=2, padx=5)
entry_start_date = tk.Entry(frame_filter)
entry_start_date.grid(row=0, column=3, padx=5)
entry_start_date.insert(0, '')

tk.Label(frame_filter, text="До:").grid(row=0, column=4, padx=5)
entry_end_date = tk.Entry(frame_filter)
entry_end_date.grid(row=0, column=5, padx=5)
entry_end_date.insert(0, '')

# Кнопка фильтрации
btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=filter_expenses)
btn_filter.grid(row=0, column=6, padx=10)

# Изначально отображать все расходы
refresh_expenses()

# Запуск интерфейса
root.mainloop()