import sqlite3
from config import DB_NAME


class SQLiteManager:
    def __init__(self):
        self.db_name = DB_NAME
        self.connect()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Connected to {self.db_name}")
        except sqlite3.Error as e:
            print("Error connecting to SQLite database:", e)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from SQLite database")

    def create_table(self, table_name, columns):
        try:

            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table '{table_name}' created successfully")
        except sqlite3.Error as e:
            print("Error creating table:", e)

    def insert_into_table(self, table_name, column_names, values):
        try:
            insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({values})"
            self.cursor.execute(insert_query)
            self.connection.commit()
            print("Data inserted into table successfully")
        except sqlite3.Error as e:
            print("Error inserting data into table:", e)

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
            return self.cursor.fetchall()  # Возвращаем результат запроса
        except sqlite3.Error as e:
            print("Error executing query:", e)
            return None  # Возвращаем None в случае ошибки


class LinksTable(SQLiteManager):
    def __init__(self):
        super().__init__()

    def create_table(self):
        super().create_table("links_gpu", "links TEXT")

    def insert_link(self, link):
        super().insert_into_table("links_gpu", "links", f"'{link}'")

    def execute_query(self, query):
        # Вызываем метод execute_query родительского класса
        # и возвращаем результат его выполнения
        return super().execute_query(query)
