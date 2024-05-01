import sqlite3
import tkinter as tk
import datetime
from tkinter import messagebox
import random
import os
import time

file_counter = 1

point_of_issue_var = None


def retrieve_products():
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("SELECT photo, name, description, manufacturer, price, quantity FROM products")
        products = cursor.fetchall()
        return products
    except Exception as e:
        print("Ошибка при получении продуктов из базы данных:", e)
    finally:
        conn.close()


def display_products():
    try:
        products = retrieve_products()

        for product in products:
            frame = tk.Frame(root)
            frame.pack(side=tk.LEFT, padx=10, pady=10)

            image = tk.PhotoImage(file=product[0])
            image_label = tk.Label(frame, image=image)
            image_label.image = image
            image_label.grid(row=0, column=0)

            name_label = tk.Label(frame, text=product[1])
            name_label.grid(row=1, column=0)

            description_label = tk.Label(frame, text=product[2])
            description_label.grid(row=2, column=0)

            manufacturer_label = tk.Label(frame, text=product[3])
            manufacturer_label.grid(row=3, column=0)

            price_label = tk.Label(frame, text=product[4])
            price_label.grid(row=4, column=0)

            quantity_label = tk.Label(frame, text=f"Количество: {product[5]}")
            quantity_label.grid(row=5, column=0)

            context_menu = tk.Menu(root, tearoff=0)
            context_menu.add_command(label="Добавить к заказу", command=lambda p=product: add_to_order(p))

            image_label.bind("<Button-3>", lambda event, menu=context_menu: (menu.post(event.x_root, event.y_root)))
            name_label.bind("<Button-3>", lambda event, menu=context_menu: (menu.post(event.x_root, event.y_root)))
            description_label.bind("<Button-3>",
                                   lambda event, menu=context_menu: (menu.post(event.x_root, event.y_root)))
            manufacturer_label.bind("<Button-3>",
                                    lambda event, menu=context_menu: (menu.post(event.x_root, event.y_root)))
            price_label.bind("<Button-3>", lambda event, menu=context_menu: (menu.post(event.x_root, event.y_root)))
            quantity_label.bind("<Button-3>",
                                lambda event, menu=context_menu: (menu.post(event.x_root, event.y_root)))

    except Exception as e:
        print("Ошибка при отображении продуктов:", e)


def add_to_order(product):
    for item in order:
        if item[:5] == product[:5]:
            item_index = order.index(item)
            order[item_index] = (*item[:5], item[5] + 1)
            print(f"Товар '{product[1]}' уже добавлен к заказу. Увеличено количество.")
            break
    else:
        order.append((*product[:5], 1))
        print(f"Добавление товара '{product[1]}' к заказу")
    view_order_button.config(state=tk.NORMAL)


def remove_from_order(product_index, order_window):
    del order[product_index]
    messagebox.showinfo("Успех", "Товар удален из заказа.")
    order_window.destroy()
    view_order()


def view_order():
    global point_of_issue_var
    order_window = tk.Toplevel(root)
    order_window.title("Просмотр заказа")

    point_of_issue_label = tk.Label(order_window, text="Выберите пункт выдачи:")
    point_of_issue_label.pack(pady=5)

    point_of_issue_var = tk.StringVar(order_window)
    point_of_issue_var.set("1")
    point_of_issue_option_menu = tk.OptionMenu(order_window, point_of_issue_var, "1", "2", "3", "4", "5")
    point_of_issue_option_menu.pack()

    for i, product in enumerate(order, start=1):
        frame = tk.Frame(order_window)
        frame.pack(padx=10, pady=5, fill=tk.X)

        image = tk.PhotoImage(file=product[0])
        image_label = tk.Label(frame, image=image)
        image_label.image = image
        image_label.pack(side=tk.LEFT)

        name_label = tk.Label(frame, text=f"{i}. Название: {product[1]}")
        name_label.pack(anchor="w")

        description_label = tk.Label(frame, text=f"Описание: {product[2]}")
        description_label.pack(anchor="w")

        manufacturer_label = tk.Label(frame, text=f"Производитель: {product[3]}")
        manufacturer_label.pack(anchor="w")

        price_label = tk.Label(frame, text=f"Цена: {product[4]}")
        price_label.pack(anchor="w")

        quantity_label = tk.Label(frame, text=f"Количество: {product[5]}")
        quantity_label.pack(anchor="w")

        remove_button = tk.Button(frame, text="Удалить", command=lambda idx=i-1, window=order_window: remove_from_order(idx, window))
        remove_button.pack(side=tk.RIGHT)

    confirm_order_button = tk.Button(order_window, text="Оформить заказ", command=confirm_order)
    confirm_order_button.pack()


def confirm_order():
    global point_of_issue_var
    confirmation_window = tk.Toplevel(root)
    confirmation_window.title("Подтверждение заказа")

    current_date = datetime.date.today()

    order_number = f"#{current_date.strftime('%Y%m%d')}"

    total_price = 0

    ordered_items = []

    for i, product in enumerate(order, start=1):
        quantity = product[5]
        ordered_items.append((*product[:5], quantity))
        total_price += product[4] * quantity

        update_product_quantity(product[1], product[5])

    order_details_text = f"Дата заказа: {current_date.strftime('%d.%m.%Y')}\n"
    order_details_text += f"Номер заказа: {order_number}\n\n"
    order_details_text += "Состав заказа:\n"
    order_details_text += "\n".join([f"{i + 1}. {item[1]} - {item[4]} руб. (Количество: {item[5]})" for i, item in
                                     enumerate(ordered_items)]) + "\n\n"
    order_details_text += f"Сумма заказа: {total_price} руб.\n\n"

    order_details_label = tk.Label(confirmation_window, text=order_details_text)
    order_details_label.pack(pady=5)

    point_of_issue = point_of_issue_var.get()

    order_details_label = tk.Label(confirmation_window, text=f"Пункт выдачи: {point_of_issue}")
    order_details_label.pack(pady=5)

    retrieval_code = ''.join([str(random.randint(0, 9)) for _ in range(3)])

    retrieval_code_label = tk.Label(confirmation_window, text=f"Код получения: **{retrieval_code}**",
                                    font=("Helvetica", 12, "bold"))
    retrieval_code_label.pack(pady=5)

    save_receipt_button = tk.Button(confirmation_window, text="Сохранить талон", command=lambda: save_receipt_as_txt(order_number, current_date, total_price, ordered_items, point_of_issue))
    save_receipt_button.pack(pady=5)

    close_button = tk.Button(confirmation_window, text="Закрыть", command=confirmation_window.destroy)
    close_button.pack(pady=5)

def update_product_quantity(product_name, quantity):
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET quantity = quantity - ? WHERE name = ?", (quantity, product_name))
        conn.commit()
    except Exception as e:
        print("Ошибка при обновлении количества товара в базе данных:", e)
    finally:
        conn.close()

def save_receipt_as_txt(order_number, current_date, total_price, ordered_items, point_of_issue):
    timestamp = int(time.time())
    filename = f"receipt_{order_number}_{timestamp}.txt"

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Дата заказа: {current_date}\n")
        file.write(f"Номер заказа: {order_number}\n")
        file.write(f"Пункт выдачи: {point_of_issue}\n\n")
        file.write("Состав заказа:\n")
        for i, item in enumerate(ordered_items, start=1):
            file.write(f"{i}. {item[1]} - {item[4]} руб. (Количество: {item[5]})\n")
        file.write(f"\nСумма заказа: {total_price} руб.")


order = []

root = tk.Tk()
root.title("Список товаров")

view_order_button = tk.Button(root, text="Просмотр заказа", command=view_order, state=tk.DISABLED)
view_order_button.pack()

display_products()
root.mainloop()
