import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Файл для хранения данных
DATA_FILE = "trainings.json"

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner - План тренировок")
        self.root.geometry("800x600")

        # Загрузка данных
        self.trainings = self.load_data()
        
        # Типы тренировок
        self.training_types = ["Бег", "Плавание", "Велосипед", "Силовая", "Йога", "Другое"]
        
        # Создание интерфейса
        self.create_input_frame()
        self.create_filter_frame()
        self.create_table_frame()
        
        # Обновление таблицы
        self.refresh_table()
    
    def load_data(self):
        """Загрузка тренировок из JSON файла"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_data(self):
        """Сохранение тренировок в JSON файл"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, indent=4, ensure_ascii=False)
    
    def create_input_frame(self):
        """Создание формы для добавления тренировок"""
        input_frame = ttk.LabelFrame(self.root, text="Добавить тренировку", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Дата
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Тип тренировки
        ttk.Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, padx=5, pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, values=self.training_types, width=15)
        self.type_combo.grid(row=0, column=3, padx=5, pady=5)
        self.type_combo.set("Бег")
        
        # Длительность
        ttk.Label(input_frame, text="Длительность (мин):").grid(row=0, column=4, padx=5, pady=5)
        self.duration_entry = ttk.Entry(input_frame, width=10)
        self.duration_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Кнопка добавления
        self.add_button = ttk.Button(input_frame, text="Добавить тренировку", command=self.add_training)
        self.add_button.grid(row=0, column=6, padx=10, pady=5)
    
    def create_filter_frame(self):
        """Создание фильтров"""
        filter_frame = ttk.LabelFrame(self.root, text="Фильтры", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Фильтр по типу
        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_type_var = tk.StringVar()
        self.filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, 
                                               values=["Все"] + self.training_types, width=15)
        self.filter_type_combo.grid(row=0, column=1, padx=5, pady=5)
        self.filter_type_combo.set("Все")
        
        # Фильтр по дате
        ttk.Label(filter_frame, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=0, column=2, padx=5, pady=5)
        self.filter_date_entry = ttk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Кнопка применения фильтра
        self.filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=self.refresh_table)
        self.filter_button.grid(row=0, column=4, padx=10, pady=5)
        
        # Кнопка сброса фильтра
        self.reset_button = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        self.reset_button.grid(row=0, column=5, padx=5, pady=5)
    
    def create_table_frame(self):
        """Создание таблицы для отображения тренировок"""
        table_frame = ttk.LabelFrame(self.root, text="Список тренировок", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Создание Treeview
        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настройка колонок
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность (мин)")
        
        self.tree.column("date", width=120)
        self.tree.column("type", width=150)
        self.tree.column("duration", width=120)
        
        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещение
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка удаления
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        self.delete_button = ttk.Button(button_frame, text="Удалить выбранную тренировку", command=self.delete_training)
        self.delete_button.pack(side="left", padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Очистить все тренировки", command=self.clear_all)
        self.clear_button.pack(side="left", padx=5)
    
    def validate_date(self, date_string):
        """Проверка корректности формата даты"""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def add_training(self):
        """Добавление новой тренировки"""
        # Получение данных
        date = self.date_entry.get().strip()
        training_type = self.type_var.get()
        duration = self.duration_entry.get().strip()
        
        # Валидация
        if not date:
            messagebox.showerror("Ошибка", "Поле 'Дата' не может быть пустым!")
            return
        
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return
        
        if not training_type:
            messagebox.showerror("Ошибка", "Выберите тип тренировки!")
            return
        
        if not duration:
            messagebox.showerror("Ошибка", "Введите длительность тренировки!")
            return
        
        try:
            duration_int = int(duration)
            if duration_int <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть целым числом!")
            return
        
        # Добавление тренировки
        training = {
            "date": date,
            "type": training_type,
            "duration": duration_int
        }
        
        self.trainings.append(training)
        self.save_data()
        self.refresh_table()
        
        # Очистка полей
        self.duration_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", "Тренировка успешно добавлена!")
    
    def refresh_table(self):
        """Обновление таблицы с учетом фильтров"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получение фильтров
        filter_type = self.filter_type_var.get()
        filter_date = self.filter_date_entry.get().strip()
        
        # Фильтрация тренировок
        filtered_trainings = self.trainings
        
        if filter_type and filter_type != "Все":
            filtered_trainings = [t for t in filtered_trainings if t["type"] == filter_type]
        
        if filter_date:
            if self.validate_date(filter_date):
                filtered_trainings = [t for t in filtered_trainings if t["date"] == filter_date]
            else:
                messagebox.showwarning("Предупреждение", "Неверный формат даты в фильтре!")
        
        # Сортировка по дате
        filtered_trainings.sort(key=lambda x: x["date"])
        
        # Добавление в таблицу
        for training in filtered_trainings:
            self.tree.insert("", "end", values=(
                training["date"],
                training["type"],
                training["duration"]
            ))
    
    def delete_training(self):
        """Удаление выбранной тренировки"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите тренировку для удаления!")
            return
        
        # Получение данных выбранной тренировки
        values = self.tree.item(selected[0])["values"]
        
        # Поиск и удаление из списка
        for i, training in enumerate(self.trainings):
            if (training["date"] == values[0] and 
                training["type"] == values[1] and 
                training["duration"] == values[2]):
                del self.trainings[i]
                break
        
        self.save_data()
        self.refresh_table()
        messagebox.showinfo("Успех", "Тренировка удалена!")
    
    def clear_all(self):
        """Очистка всех тренировок"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить все тренировки?"):
            self.trainings = []
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Успех", "Все тренировки удалены!")
    
    def reset_filter(self):
        """Сброс фильтров"""
        self.filter_type_var.set("Все")
        self.filter_date_entry.delete(0, tk.END)
        self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
