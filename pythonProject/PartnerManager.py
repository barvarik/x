import tkinter as tk
from gui import PartnerListWindow, AddPartnerWindow
from database import DatabaseManager
from ttkthemes import ThemedTk

def main():
    connection_params = {
        "host": "localhost",
        "port": 5432,
        "database": "postgres",
        "user": "postgres",
        "password": ""
    }

    db_manager = DatabaseManager(connection_params)

    root = tk.Tk()

    def open_add_partner_window():
        """Открывает окно добавления партнера."""
        AddPartnerWindow(root, db_manager, partner_list_window.load_partners)

    partner_list_window = PartnerListWindow(root, db_manager, open_add_partner_window)

    root.mainloop()

if __name__ == "__main__":
    main()