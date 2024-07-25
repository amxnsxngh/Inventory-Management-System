import sqlite3
from tabulate import tabulate


class Store:
    def addproduct(self, name, price, quantity):
        c.execute("""INSERT INTO product (productName, productPrice, productQuantity)
        VALUES (? , ?, ?)""", (name, price, quantity))
        conn.commit()

    def removeproduct(self, product_id):
        c.execute("DELETE FROM product WHERE productID = ?", (product_id,))
        conn.commit()

    def updateproduct(self, product_id, name, price, quantity):
        c.execute("""UPDATE product SET productName=?, productPrice=?, productQuantity=? WHERE productID=?""",
                  (name, price, quantity, product_id))
        conn.commit()

    def displayproduct(self):
        c.execute('SELECT * FROM product')
        products = c.fetchall()
        if not products:
            print("No products in the inventory.")
            return
        headers = ['Product ID', 'Name', 'Price', 'Quantity']
        print(tabulate(products, headers=headers, tablefmt='fancy_grid'))

    def sellproduct(self, product_id, sale_date, sale_quantity):
        c.execute("""SELECT productQuantity FROM product WHERE productID=?""",
                  (product_id,))
        row = c.fetchone()
        if row is None:
            print('Product does not exist')
            return
        available_quant = row[0]
        if available_quant < sale_quantity:
            print('Insufficient quantity of product in stock.')
            return
        updated_quantity = available_quant - sale_quantity
        c.execute("""UPDATE product SET productQuantity=? WHERE productID=?""",
                  (updated_quantity, product_id))
        c.execute("SELECT productPrice FROM product WHERE productID=?", (product_id,))
        sale_total = c.fetchone()[0] * sale_quantity
        c.execute("""INSERT INTO sales (saleDate, productName, saleTotal)
        VALUES (?, (SELECT productName FROM product WHERE productID=?), ?)""",
                  (sale_date, product_id, sale_total))
        print('Sale successful')
        conn.commit()


conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute("""CREATE TABLE product (
    productID INTEGER PRIMARY KEY,
    productName TEXT,
    productPrice REAL,
    productQuantity INTEGER
    )""")
conn.commit()

c.execute("""CREATE TABLE sales (
    saleID INTEGER PRIMARY KEY,
    saleDate TEXT,
    productName TEXT,
    saleTotal INTEGER,
    FOREIGN KEY(productName) REFERENCES product(productName)
    )""")
conn.commit()

while True:

    store = Store()

    print("Welcome to the Inventory management System, please select what you would like to do:")
    print("""
    1. Add Product
    2. Remove Product
    3. Update Product
    4. Display Product
    5. Sell Product
    6. Exit
    """)
    user_choice = input('Enter Your Choice: ')

    if user_choice == '1':
        name = input("Enter product name: ")
        price = float(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))
        store.addproduct(name, price, quantity)

    elif user_choice == '2':
        product_id = int(input("Enter Product ID: "))
        store.removeproduct(product_id)

    elif user_choice == '3':
        product_id = int(input("Enter product ID to update:"))
        name = input('Enter new product name: ')
        price = float(input("Enter new product price: "))
        quantity = int(input("Enter new product quantity: "))
        store.updateproduct(product_id, name, price, quantity)

    elif user_choice == '4':
        store.displayproduct()

    elif user_choice == '5':
        product_id = int(input("Enter product ID to sell: "))
        sale_date = input('Enter the date "(YYY-MM-DD)": ')
        sale_quantity = int(input("Enter sale quantity: "))
        store.sellproduct(product_id, sale_date, sale_quantity)

    elif user_choice == '6':
        conn.close()
        print('Bye Bye')
        break


