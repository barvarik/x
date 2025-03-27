import psycopg2

class DatabaseManager:
    def __init__(self, connection_params):
        self.connection_params = connection_params

    def connect(self):
        """Устанавливает соединение с базой данных."""
        try:
            self.conn = psycopg2.connect(client_encoding='utf8', **self.connection_params)
            self.cur = self.conn.cursor()
            return True
        except psycopg2.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            return False

    def disconnect(self):
        """Закрывает соединение с базой данных."""
        if hasattr(self, 'cur'):
            self.cur.close()
        if hasattr(self, 'conn'):
            self.conn.close()

    def fetch_partners(self):
        """Получает список партнеров из базы данных с типом партнера."""
        try:
            if not hasattr(self, 'conn') or self.conn.closed:
                if not self.connect():
                    return []

            self.cur.execute("""
                SELECT p.partner_id, p.partner_name, p.partner_direct, p.partner_mail, p.partner_phone, p.partner_address, pt.partner_tipe, p.partner_top, p.partner_inn, p.tipe_id
                FROM partners p
                JOIN partner_tipe pt ON p.tipe_id = pt.tipe_id;
            """)
            partners = []
            for row in self.cur.fetchall():
                partners.append({
                    'partner_id': row[0],
                    'partner_name': row[1],
                    'partner_direct': row[2],
                    'partner_mail': row[3],
                    'partner_phone': row[4],
                    'partner_address': row[5],
                    'partner_tipe': row[6],
                    'partner_top': row[7],
                    'partner_inn': row[8],
                    'tipe_id': row[9]
                })
            return partners
        except psycopg2.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return []

    def fetch_partner_types(self):
        """Получает список типов партнеров из базы данных."""
        try:
            if not hasattr(self, 'conn') or self.conn.closed:
                if not self.connect():
                    return []

            self.cur.execute("SELECT tipe_id, partner_tipe FROM partner_tipe;")
            partner_types = []
            for row in self.cur.fetchall():
                partner_types.append({
                    'tipe_id': row[0],
                    'partner_tipe': row[1]
                })
            return partner_types
        except psycopg2.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return []

    def calculate_discount(self, partner_id):
        """Рассчитывает скидку для партнера."""
        try:
            if not hasattr(self, 'conn') or self.conn.closed:
                if not self.connect():
                    return 0.0

            self.cur.execute("SELECT SUM(kolvo_product) FROM partner_product WHERE partner_id = %s;", (partner_id,))
            result = self.cur.fetchone()
            total_sales = float(result[0]) if result[0] else 0.0
            if total_sales < 10000:
                return 0.0
            elif 10000 <= total_sales < 50000:
                return 5.0
            elif 50000 <= total_sales < 300000:
                return 10.0
            else:
                return 15.0
        except psycopg2.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return 0.0

    def add_partner(self, partner_data):
        """Добавляет нового партнера в базу данных."""
        try:
            if not hasattr(self, 'conn') or self.conn.closed:
                if not self.connect():
                    return False

            try:
                partner_phone = int(partner_data['partner_phone'])
                tipe_id = int(partner_data['tipe_id'])
                partner_top = int(partner_data['partner_top'])
                partner_inn = str(partner_data['partner_inn'])
            except ValueError as e:
                print(f"Ошибка типа данных: {e}")
                return False

            print("Данные для INSERT:", partner_data)  # Debug вывод

            self.cur.execute("""
                INSERT INTO partners (partner_name, partner_direct, partner_mail, partner_phone, partner_address, tipe_id, partner_top, partner_inn)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                partner_data['partner_name'],
                partner_data['partner_direct'],
                partner_data['partner_mail'],
                partner_phone,
                partner_data['partner_address'],
                tipe_id,
                partner_top,
                partner_inn
            ))

            self.conn.commit()
            print("Партнер успешно добавлен в базу данных.")  # Debug
            return True
        except psycopg2.Error as e:
            print(f"Ошибка при добавлении партнера: {e}")
            self.conn.rollback()
            return False

    def update_partner(self, partner_id, partner_data):
        """Обновляет данные партнера в базе данных."""
        try:
            if not hasattr(self, 'conn') or self.conn.closed:
                if not self.connect():
                    return False

            self.cur.execute("""
                UPDATE partners
                SET partner_name = %s, partner_direct = %s, partner_mail = %s, partner_phone = %s,
                    partner_address = %s, tipe_id = %s, partner_top = %s, partner_inn = %s
                WHERE partner_id = %s;
            """, (
                partner_data['partner_name'],
                partner_data['partner_direct'],
                partner_data['partner_mail'],
                partner_data['partner_phone'],
                partner_data['partner_address'],
                partner_data['tipe_id'],
                partner_data['partner_top'],
                partner_data['partner_inn'],
                partner_id
            ))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Ошибка при обновлении партнера: {e}")
            self.conn.rollback()
            return False