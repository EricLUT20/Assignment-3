import psycopg2
from psycopg2 import sql

def databaseCreation(dbname):
    try:
        postgres_database = psycopg2.connect(dbname="postgres", user="postgres", password="admin", host="localhost", port="5432")
        postgres_database.autocommit = True
        with postgres_database.cursor() as cursor:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
        postgres_database.close()
        print(f"Database '{dbname}' created successfully.\n")
    except Exception as error:
        print(f"Error creating database '{dbname}': {error}")

def tableCreation(dbname, location):
    active_db = psycopg2.connect(dbname=dbname, user="postgres", password="admin", host="localhost", port="5432")
    try: 
        with active_db.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE Products (
                    product_id SERIAL PRIMARY KEY,
                    product_name VARCHAR(100),
                    description TEXT,
                    price DECIMAL,
                    stock_quantity INT
                );
            """)

            cursor.execute("""
                CREATE TABLE Customers (
                    customer_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    email_address VARCHAR(100),
                    shipping_address TEXT
                );
            """)

            cursor.execute("""
                CREATE TABLE Orders (
                    order_id SERIAL PRIMARY KEY,
                    customer_id INT,
                    order_date DATE,
                    shipping_date DATE,
                    total_amount DECIMAL,
                    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
                );
            """)

            cursor.execute("""
                CREATE TABLE Payments (
                    payment_id SERIAL PRIMARY KEY,
                    order_id INT,
                    payment_date DATE,
                    payment_method VARCHAR(50),
                    amount_paid DECIMAL,
                    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE
                );
            """)

            if location == "Helsinki":
                cursor.execute("""
                    INSERT INTO Customers (first_name, last_name, email_address, shipping_address) VALUES
                    ('Alice', 'Johnson', 'alice.johnson@gmail.com', 'Helsinki, Finland'),
                    ('Bob', 'Smith', 'bob.smith@gmail.com', 'Helsinki, Finland'),
                    ('Charlie', 'Brown', 'charlie.brown@gmail.com', 'Helsinki, Finland'),
                    ('David', 'White', 'david.white@gmail.com', 'Helsinki, Finland'),
                    ('Eva', 'Green', 'eva.green@gmail.com', 'Helsinki, Finland');
                """)

            elif location == "LPR":
                cursor.execute("""
                    INSERT INTO Customers (first_name, last_name, email_address, shipping_address) VALUES
                    ('Frank', 'Black', 'frank.black@gmail.com', 'LPR, Finland'),
                    ('Grace', 'Gray', 'grace.gray@gmail.com', 'LPR, Finland'),
                    ('Hank', 'Yellow', 'hank.yellow@gmail.com', 'LPR, Finland'),
                    ('Ivy', 'Blue', 'ivy.blue@gmail.com', 'LPR, Finland'),
                    ('Jack', 'Purple', 'jack.purple@gmail.com', 'LPR, Finland');
                """)

            elif location == "Turku":
                cursor.execute("""
                    INSERT INTO Customers (first_name, last_name, email_address, shipping_address) VALUES
                    ('Kathy', 'Red', 'kathy.red@gmail.com', 'Turku, Finland'),
                    ('Liam', 'Orange', 'liam.orange@gmail.com', 'Turku, Finland'),
                    ('Mona', 'Pink', 'mona.pink@gmail.com', 'Turku, Finland'),
                    ('Nina', 'Brown', 'nina.brown@gmail.com', 'Turku, Finland'),
                    ('Oscar', 'Green', 'oscar.green@gmail.com', 'Turku, Finland');
                """)

            cursor.execute("""
                INSERT INTO Products (product_name, description, price, stock_quantity) VALUES
                ('Laptop', 'Asus Gaming laptop', 1200.00, 50),
                ('Phone', 'iPhone 15', 1000.00, 100),
                ('Tablet', 'iPad', 500.00, 75),
                ('Monitor', 'BenQ 360hz monitor', 540.00, 150),
                ('Headphones', 'Logitech G Pro', 100.00, 200);
            """)

            if location == "Helsinki":
                cursor.execute("""
                    INSERT INTO Orders (customer_id, order_date, shipping_date, total_amount) VALUES
                    (1, '2024-11-15', '2024-11-17', 1200.00),
                    (2, '2024-11-16', '2024-11-18', 800.00),
                    (3, '2024-11-17', '2024-11-19', 500.00),
                    (4, '2024-11-18', '2024-11-20', 300.00),
                    (5, '2024-11-19', '2024-11-21', 50.00);
                """)
            elif location == "LPR":
                cursor.execute("""
                    INSERT INTO Orders (customer_id, order_date, shipping_date, total_amount) VALUES
                    (1, '2024-11-17', '2024-11-19', 800.00),
                    (2, '2024-11-18', '2024-11-20', 1200.00),
                    (3, '2024-11-19', '2024-11-21', 300.00),
                    (4, '2024-11-20', '2024-11-22', 500.00),
                    (5, '2024-11-21', '2024-11-23', 150.00);
                """)
            elif location == "Turku":
                cursor.execute("""
                    INSERT INTO Orders (customer_id, order_date, shipping_date, total_amount) VALUES
                    (1, '2024-11-18', '2024-11-20', 50.00),
                    (2, '2024-11-19', '2024-11-21', 200.00),
                    (3, '2024-11-20', '2024-11-22', 100.00),
                    (4, '2024-11-21', '2024-11-23', 500.00),
                    (5, '2024-11-22', '2024-11-24', 300.00);
                """)

            cursor.execute("""
                INSERT INTO Payments (order_id, payment_date, payment_method, amount_paid) VALUES
                (1, '2024-11-15', 'Credit Card', 1200.00),
                (2, '2024-11-16', 'PayPal', 800.00),
                (3, '2024-11-17', 'Credit Card', 500.00),
                (4, '2024-11-18', 'Bank Transfer', 300.00),
                (5, '2024-11-19', 'Credit Card', 50.00);
            """)

            active_db.commit()
        print(f"Tables created in '{dbname}' successfully.\n")

    except Exception as error:
        active_db.rollback()
        print(f"Error creating tables in '{dbname}': {error}")
    
    active_db.close()


def main():
    print("-------------------------------------------")
    print("###### Creating databases ######")
    print("-------------------------------------------\n")
    try:
        databaseCreation("helsinki_db")

    except Exception as error:
        print(f"Error creating database 'helsinki_db': {error}")
    try:
        databaseCreation("lpr_db")

    except Exception as error:
        print(f"Error creating database 'lpr_db': {error}")
    try:
        databaseCreation("turku_db")

    except Exception as error:
        print(f"Error creating database 'turku_db': {error}")

    print("-------------------------------------------")
    print("###### Creating tables ######")
    print("-------------------------------------------\n")

    try:
        tableCreation("helsinki_db", "Helsinki")

    except Exception as error:
        print(f"Error creating tables in 'helsinki_db': {error}")
    try:
        tableCreation("lpr_db", "LPR")

    except Exception as error:
        print(f"Error creating tables in 'lpr_db': {error}")
    try:
        tableCreation("turku_db", "Turku")

    except Exception as error:
        print(f"Error creating tables in 'turku_db': {error}")

    print("-------------------------------------------\n")

if __name__ == "__main__":
    main()