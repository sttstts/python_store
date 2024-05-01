import sqlite3

def create_database():
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS products
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           photo TEXT,
                           name TEXT,
                           description TEXT,
                           manufacturer TEXT,
                           price REAL,
                           quantity INTEGER)''')

        conn.commit()
        print("База данных успешно создана!")
    except Exception as e:
        print("Ошибка при создании базы данных:", e)
    finally:
        conn.close()

def add_product(photo, name, description, manufacturer, price, quantity):
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO products (photo, name, description, manufacturer, price, quantity)
                          VALUES (?, ?, ?, ?, ?, ?)''', (photo, name, description, manufacturer, price, quantity))

        conn.commit()
        print("Продукт успешно добавлен в базу данных!")
    except Exception as e:
        print("Ошибка при добавлении продукта в базу данных:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()
    add_product("image/apple.png", "Яблоки", "сладкие", "Сады придонии", 10, 100)
    add_product("image/detergent.png", "Моющее средство", "фери", "Procter and Gamble", 110, 50)
    add_product("image/yogurt.png", "Йогурт", "клубничный", "Простоквашино ", 20, 200)
    add_product("image/soda.png", "Лимонад", "фрешбар", "Global Functional Drinks ", 92, 75)
    add_product("image/juice.png", "Сок", "мультифрукт", "МУЛТОН ПАРТНЕРС ", 231, 30)
