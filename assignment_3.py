import psycopg2

helsinki_db = psycopg2.connect(
    dbname="helsinki_db",
    user="postgres",
    host="localhost",
    password="admin",
    port=5432
)

lpr_db = psycopg2.connect(
    dbname="lpr_db",
    user="postgres",
    host="localhost",
    password="admin",
    port=5432
)

turku_db = psycopg2.connect(
    dbname="turku_db",
    user="postgres",
    host="localhost",
    password="admin",
    port=5432
)

def menu():
    print("1. Change location (Helsinki, LPR, Turku)")
    print("2. Print tables")
    print("3. Run a query")
    print("0. Exit")

def main():
    active_db = None
    print("-------------------------------------------")
    print("###### Postgres Database Application ######")
    print("-------------------------------------------\n")

    while (active_db == None):
        try:
            location = input("Select a location (Helsinki, LPR, Turku): ").lower()
            if location == "helsinki":
                active_db = helsinki_db
                print("Switched to Helsinki database.\n")
            elif location == "lpr":
                active_db = lpr_db
                print("Switched to Lappeenranta database.\n")
            elif location == "turku":
                active_db = turku_db
                print("Switched to Turku database.\n")
            else:
                print("Invalid location. Try again.\n")
        except Exception as error:
            print(f"Error: {error}")

    while True:
        menu()
        choice = None
        try: 
            choice = int(input("\nEnter your choice: "))
        except Exception as error:
            print(f"Error: {error}")
        print()
        if choice == 1:
            location = input("Enter location (Helsinki, LPR, Turku): ").lower()
            if location == "helsinki":
                active_db = helsinki_db
                print("Switched to Helsinki database.\n")
            elif location == "lpr":
                active_db = lpr_db
                print("Switched to Lappeenranta database.\n")
            elif location == "turku":
                active_db = turku_db
                print("Switched to Turku database.\n")
            else:
                print("Invalid location. Try again.\n")
        
        elif choice == 2:
            try:
                with active_db.cursor() as cursor:
                    cursor.execute("""
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public'
                        ORDER BY table_name;
                    """)
                    tables = cursor.fetchall()
                    if tables:
                        print("Tables in the current database:")
                        for table in tables:
                            print(table[0])
                    else:
                        print("No tables exist")
                    print()
            except Exception as error:
                print(f"Error: {error}")
        
        elif choice == 3:
            query = input("Enter a query: ")
            try:
                with active_db.cursor() as cursor:
                    cursor.execute(query)
                    if query.lower().startswith("select"):
                        rows = cursor.fetchall()
                        for row in rows:
                            print(row)
                    else:
                        active_db.commit()
                        print("Query executed successfully.")   
                print()
            except Exception as error:
                active_db.rollback()
                print(f"Error: {error}")

        elif choice == 0:
            print("Exiting the application...\n")
            break
        
        else:
            print("Invalid choice. Try again.\n")
    helsinki_db.close()
    lpr_db.close()
    turku_db.close()

if __name__ == "__main__":
    main()