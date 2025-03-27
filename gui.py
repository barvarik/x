import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager
import platform
# --- Цвета ---
BG_COLOR = "white"
SECONDARY_BG_COLOR = "#F4E8D3"
ACCENT_COLOR = "#67BA80"

# --- Шрифты ---
FONT_FAMILY = "Segoe UI"
DEFAULT_FONT = (FONT_FAMILY, 10)
BOLD_FONT = (FONT_FAMILY, 12, 'bold')

class PartnerCard(tk.Frame):
    def __init__(self, parent, partner_data, discount, on_edit):
        super().__init__(parent, padx=10, pady=10, relief=tk.GROOVE, borderwidth=1)
        self.partner_data = partner_data
        self.discount = discount
        self.on_edit = on_edit
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Информация о партнере", font=BOLD_FONT, bg=SECONDARY_BG_COLOR).grid(row=0, column=0,
                                                                                                 sticky=tk.W,
                                                                                                 columnspan=3,
                                                                                                 pady=(0, 5))

        tk.Label(self, text=f"{self.partner_data.get('partner_tipe', 'Тип')} | {self.partner_data['partner_name']}",
                 font=BOLD_FONT, bg=SECONDARY_BG_COLOR).grid(row=1, column=0, sticky=tk.W, columnspan=2)
        tk.Label(self, text=f"Директор: {self.partner_data['partner_direct']}", font=DEFAULT_FONT,
                 bg=SECONDARY_BG_COLOR).grid(row=2, column=0, sticky=tk.W, columnspan=2)
        tk.Label(self, text=f"Телефон: {self.partner_data['partner_phone']}", font=DEFAULT_FONT,
                 bg=SECONDARY_BG_COLOR).grid(row=3, column=0, sticky=tk.W, columnspan=2)
        tk.Label(self, text=f"Рейтинг: {self.partner_data['partner_top']}", font=DEFAULT_FONT,
                 bg=SECONDARY_BG_COLOR).grid(row=4, column=0, sticky=tk.W, columnspan=2)
        tk.Label(self, text=f"ИНН: {self.partner_data['partner_inn']}", font=DEFAULT_FONT, bg=SECONDARY_BG_COLOR).grid(
            row=5, column=0, sticky=tk.W, columnspan=2)
        tk.Label(self, text=f"{self.discount:.0f}%", font=DEFAULT_FONT, bg=SECONDARY_BG_COLOR).grid(row=1, column=2,
                                                                                                    sticky=tk.E)

        edit_button = tk.Button(self, text="Редактировать", command=self.edit_partner, bg=ACCENT_COLOR, fg="white",
                                font=DEFAULT_FONT)
        edit_button.grid(row=6, column=0, columnspan=3, pady=5)

    def edit_partner(self):
        self.on_edit(self.partner_data)

class PartnerListWindow:
    def __init__(self, root, db_manager, open_add_partner_window):
        self.root = root
        self.root.title("Управление партнерами")
        self.db_manager = db_manager
        self.partner_frames = []
        self.open_add_partner_window = open_add_partner_window
        self.create_widgets()
        self.load_partners()
        try:
            if platform.system() == 'Windows':
                self.root.iconbitmap("resources/icon.ico")  # Для Windows
            else:
                #  Попытка использовать .png (более кроссплатформенный вариант)
                img = tk.PhotoImage(file="resources/icon.png")
                self.root.tk.call('wm', 'iconphoto', self.root._w, img)
        except tk.TclError:
            print("Не удалось загрузить иконку. Убедитесь, что файл icon.ico (или icon.png) существует.")


    def create_widgets(self):
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        add_button = tk.Button(self.root, text="Добавить партнера", command=self.open_add_partner_window,
                               bg=ACCENT_COLOR, fg="white", font=DEFAULT_FONT)
        add_button.pack(pady=10)

    def load_partners(self):
        partners = self.db_manager.fetch_partners()

        if not partners:
            print("Не удалось получить список партнеров из базы данных.")
            return

        for frame in self.partner_frames:
            frame.destroy()
        self.partner_frames = []

        row_num = 0
        for partner in partners:
            discount = self.db_manager.calculate_discount(partner['partner_id'])
            card = PartnerCard(self.scrollable_frame, partner, discount, on_edit=self.open_edit_partner_window)
            card.grid(row=row_num, column=0, padx=5, pady=5, sticky="ew")
            self.partner_frames.append(card)
            row_num += 1

    def open_edit_partner_window(self, partner_data):
        EditPartnerWindow(self.root, self.db_manager, partner_data, self.load_partners)

class AddPartnerWindow:
    def __init__(self, root, db_manager, refresh_partner_list):
        self.root = tk.Toplevel(root)
        self.root.title("Добавить партнера")
        self.db_manager = db_manager
        self.refresh_partner_list = refresh_partner_list
        self.partner_data = {}
        self.create_widgets()
        try:
            if platform.system() == 'Windows':
                self.root.iconbitmap("resources/icon.ico")  # Для Windows
            else:
                #  Попытка использовать .png (более кроссплатформенный вариант)
                img = tk.PhotoImage(file="resources/icon.png")
                self.root.tk.call('wm', 'iconphoto', self.root._w, img)
        except tk.TclError:
            print("Не удалось загрузить иконку. Убедитесь, что файл icon.ico (или icon.png) существует.")

    def create_widgets(self):
        tk.Label(self.root, text="Информация о партнере", font=BOLD_FONT, bg=BG_COLOR).grid(row=0, column=0,
                                                                                            sticky=tk.W, columnspan=2,
                                                                                            pady=(10, 5))

        tk.Label(self.root, text="Наименование:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=1, column=0, sticky=tk.W,
                                                                                       padx=5, pady=5)
        tk.Label(self.root, text="Тип партнера:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=2, column=0, sticky=tk.W,
                                                                                       padx=5, pady=5)
        tk.Label(self.root, text="Рейтинг:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=3, column=0, sticky=tk.W, padx=5,
                                                                                  pady=5)
        tk.Label(self.root, text="Адрес:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=4, column=0, sticky=tk.W, padx=5,
                                                                                pady=5)
        tk.Label(self.root, text="ФИО директора:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=5, column=0, sticky=tk.W,
                                                                                        padx=5, pady=5)
        tk.Label(self.root, text="Телефон:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=6, column=0, sticky=tk.W, padx=5,
                                                                                  pady=5)
        tk.Label(self.root, text="Email:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=7, column=0, sticky=tk.W, padx=5,
                                                                                pady=5)
        tk.Label(self.root, text="ИНН:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=8, column=0, sticky=tk.W, padx=5,
                                                                              pady=5)

        self.name_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.name_entry.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)

        partner_types = self.db_manager.fetch_partner_types()
        type_names = [partner_type['partner_tipe'] for partner_type in partner_types]
        self.type_id_mapping = {partner_type['partner_tipe']: partner_type['tipe_id'] for partner_type in partner_types}

        self.type_combo = ttk.Combobox(self.root, values=type_names, state="readonly", font=DEFAULT_FONT)
        self.type_combo.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)
        if type_names:
            self.type_combo.current(0)

        self.rating_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.rating_entry.grid(row=3, column=1, sticky=tk.E, padx=5, pady=5)

        self.address_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.address_entry.grid(row=4, column=1, sticky=tk.E, padx=5, pady=5)

        self.director_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.director_entry.grid(row=5, column=1, sticky=tk.E, padx=5, pady=5)

        self.phone_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.phone_entry.grid(row=6, column=1, sticky=tk.E, padx=5, pady=5)

        self.email_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.email_entry.grid(row=7, column=1, sticky=tk.E, padx=5, pady=5)

        self.inn_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.inn_entry.grid(row=8, column=1, sticky=tk.E, padx=5, pady=5)

        save_button = tk.Button(self.root, text="Сохранить", command=self.save_partner, bg=ACCENT_COLOR, fg="white",
                                font=DEFAULT_FONT)
        save_button.grid(row=9, column=0, columnspan=2, pady=5)

    def load_partner_data(self):
        self.name_entry.insert(0, self.partner_data['partner_name'])

        # Get type_id
        selected_type = next(
            (key for key, value in self.type_id_mapping.items() if value == self.partner_data['tipe_id']), None)

        if selected_type:
            self.type_combo.set(selected_type)
        else:
            print("Partner type not found")

        self.rating_entry.insert(0, str(self.partner_data['partner_top']))
        self.address_entry.insert(0, self.partner_data['partner_address'])
        self.director_entry.insert(0, self.partner_data['partner_direct'])
        self.phone_entry.insert(0, self.partner_data['partner_phone'])
        self.email_entry.insert(0, self.partner_data['partner_mail'])
        self.inn_entry.insert(0, self.partner_data['partner_inn'])

    def save_partner(self):
        try:
            name = self.name_entry.get()
            selected_type = self.type_combo.get()
            rating_str = self.rating_entry.get()
            address = self.address_entry.get()
            director = self.director_entry.get()
            phone_str = self.phone_entry.get()
            email = self.email_entry.get()
            inn = self.inn_entry.get()

            if not all([name, selected_type, rating_str, address, director, phone_str, email, inn]):
                messagebox.showerror("Ошибка", "Заполните все поля.")
                return

            try:
                rating = int(rating_str)
                if rating < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Рейтинг должен быть целым неотрицательным числом.")
                return

            try:
                phone = int(phone_str)
            except ValueError:
                messagebox.showerror("Ошибка", "Телефон должен содержать только цифры.")
                return

            if not inn.isdigit():
                messagebox.showerror("Ошибка", "ИНН должен содержать только цифры.")
                return

            type_id = self.type_id_mapping[selected_type]

            partner_data = {
                'partner_name': name,
                'partner_direct': director,
                'partner_mail': email,
                'partner_phone': phone_str,
                'partner_address': address,
                'tipe_id': type_id,
                'partner_top': rating,
                'partner_inn': inn
            }

            if self.db_manager.add_partner(partner_data):
                messagebox.showinfo("Информация", "Партнер успешно добавлен.")
                self.refresh_partner_list()
                self.root.destroy()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить партнера.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {e}")

class EditPartnerWindow:
    def __init__(self, root, db_manager, partner_data, refresh_partner_list):
        self.root = tk.Toplevel(root)
        self.root.title("Редактировать партнера")
        self.db_manager = db_manager
        self.partner_data = partner_data
        self.refresh_partner_list = refresh_partner_list
        self.create_widgets()
        self.load_partner_data()
        try:
            if platform.system() == 'Windows':
                self.root.iconbitmap("resources/icon.ico")  # Для Windows
            else:
                #  Попытка использовать .png (более кроссплатформенный вариант)
                img = tk.PhotoImage(file="resources/icon.png")
                self.root.tk.call('wm', 'iconphoto', self.root._w, img)
        except tk.TclError:
            print("Не удалось загрузить иконку. Убедитесь, что файл icon.ico (или icon.png) существует.")

    def create_widgets(self):
        tk.Label(self.root, text="Информация о партнере", font=BOLD_FONT, bg=BG_COLOR).grid(row=0, column=0,
                                                                                            sticky=tk.W, columnspan=2,
                                                                                            pady=(10, 5))

        tk.Label(self.root, text="Наименование:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=1, column=0, sticky=tk.W,
                                                                                       padx=5, pady=5)
        tk.Label(self.root, text="Тип партнера:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=2, column=0, sticky=tk.W,
                                                                                       padx=5, pady=5)
        tk.Label(self.root, text="Рейтинг:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=3, column=0, sticky=tk.W, padx=5,
                                                                                  pady=5)
        tk.Label(self.root, text="Адрес:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=4, column=0, sticky=tk.W, padx=5,
                                                                                pady=5)
        tk.Label(self.root, text="ФИО директора:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=5, column=0, sticky=tk.W,
                                                                                        padx=5, pady=5)
        tk.Label(self.root, text="Телефон:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=6, column=0, sticky=tk.W, padx=5,
                                                                                  pady=5)
        tk.Label(self.root, text="Email:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=7, column=0, sticky=tk.W, padx=5,
                                                                                pady=5)
        tk.Label(self.root, text="ИНН:", bg=BG_COLOR, font=DEFAULT_FONT).grid(row=8, column=0, sticky=tk.W, padx=5,
                                                                              pady=5)

        self.name_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.name_entry.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)

        partner_types = self.db_manager.fetch_partner_types()
        type_names = [partner_type['partner_tipe'] for partner_type in partner_types]
        self.type_id_mapping = {partner_type['partner_tipe']: partner_type['tipe_id'] for partner_type in partner_types}

        self.type_combo = ttk.Combobox(self.root, values=type_names, state="readonly", font=DEFAULT_FONT)
        self.type_combo.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)
        if type_names:
            self.type_combo.current(0)

        self.rating_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.rating_entry.grid(row=3, column=1, sticky=tk.E, padx=5, pady=5)

        self.address_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.address_entry.grid(row=4, column=1, sticky=tk.E, padx=5, pady=5)

        self.director_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.director_entry.grid(row=5, column=1, sticky=tk.E, padx=5, pady=5)

        self.phone_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.phone_entry.grid(row=6, column=1, sticky=tk.E, padx=5, pady=5)

        self.email_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.email_entry.grid(row=7, column=1, sticky=tk.E, padx=5, pady=5)

        self.inn_entry = tk.Entry(self.root, font=DEFAULT_FONT)
        self.inn_entry.grid(row=8, column=1, sticky=tk.E, padx=5, pady=5)

        save_button = tk.Button(self.root, text="Сохранить", command=self.save_partner, bg=ACCENT_COLOR, fg="white",
                                font=DEFAULT_FONT)
        save_button.grid(row=9, column=0, columnspan=2, pady=5)

    def load_partner_data(self):
        self.name_entry.insert(0, self.partner_data['partner_name'])

        # Get type_id
        selected_type = next((key for key, value in self.type_id_mapping.items() if value == self.partner_data['tipe_id']), None)

        if selected_type:
            self.type_combo.set(selected_type)
        else:
            print("Partner type not found")

        self.rating_entry.insert(0, str(self.partner_data['partner_top']))
        self.address_entry.insert(0, self.partner_data['partner_address'])
        self.director_entry.insert(0, self.partner_data['partner_direct'])
        self.phone_entry.insert(0, self.partner_data['partner_phone'])
        self.email_entry.insert(0, self.partner_data['partner_mail'])
        self.inn_entry.insert(0, self.partner_data['partner_inn'])

    def _update_partner_data(self, partner_id, partner_data):
        """Вспомогательная функция для обновления данных партнера."""
        try:
            return self.db_manager.update_partner(partner_id, partner_data)
        except AttributeError:
            messagebox.showerror("Ошибка", "Не удалось обновить партнера. Метод update_partner отсутствует.")
            return False
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при обновлении: {e}")
            return False


    def save_partner(self):
        try:
            name = self.name_entry.get()
            selected_type = self.type_combo.get()
            rating_str = self.rating_entry.get()
            address = self.address_entry.get()
            director = self.director_entry.get()
            phone_str = self.phone_entry.get()
            email = self.email_entry.get()
            inn = self.inn_entry.get()

            if not all([name, selected_type, rating_str, address, director, phone_str, email, inn]):
                messagebox.showerror("Ошибка", "Заполните все поля.")
                return

            try:
                rating = int(rating_str)
                if rating < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Рейтинг должен быть целым неотрицательным числом.")
                return

            try:
                phone = int(phone_str)
            except ValueError:
                messagebox.showerror("Ошибка", "Телефон должен содержать только цифры.")
                return

            if not inn.isdigit():
                messagebox.showerror("Ошибка", "ИНН должен содержать только цифры.")
                return

            type_id = self.type_id_mapping[selected_type]

            partner_data = {
                'partner_name': name,
                'partner_direct': director,
                'partner_mail': email,
                'partner_phone': phone_str,
                'partner_address': address,
                'tipe_id': type_id,
                'partner_top': rating,
                'partner_inn': inn
            }

            if self._update_partner_data(self.partner_data['partner_id'], partner_data): # Используем вспомогательную функцию
                messagebox.showinfo("Информация", "Партнер успешно обновлен.")
                self.refresh_partner_list()
                self.root.destroy()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить партнера.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {e}")
