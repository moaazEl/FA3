import csv, sqlite3,os

if os.path.isfile("jer.db"):
    os.remove('jer.db')

def create_customers_table():
    con = sqlite3.connect("jer.db")
    cur = con.cursor()

    cur.execute("""
        create table customers(
        customer_id integer PRIMARY KEY autoincrement,
        address text not null,
        first text not null,
        surname text not null,
        phone text not null,
        dob text,
        FOREIGN KEY (tran) REFERENCES sales(tran),
        email text not null,
        password text not null
        );""")
    reader = csv.reader(open('cus.csv', 'r'),delimiter=',')
    next(reader)
    for row in reader:
        print(row)
        to_db = [ row[1], row[2], row[3], row[7], row[4], row[5], row[6], row[7]]
        cur.execute('''INSERT INTO customers (first, surname, dob, email, phone, address, tran, password)
                       VALUES ( ?, ?, ?, ?, ?, ?, ?, ?);''', to_db)
    cur.execute("UPDATE cusomers SET password = 'Password@45';") 
    con.commit()
    con.close()
    return 'cus.csv processed and data inserted into database.'
    con.commit()
    con.close()

#def create_customer_table():
#    con = sqlite3.connect("jer.db")
#    cur = con.cursor()
#
#    cur.execute("""
#        create table customers (
#        customer_id integer primary key autoincrement,
#        first text not null,
#        surname text not null,
#        phone# text not null,
#        dob text,
#        address text not null,
#        tran# integer not null,
#        email text not null );""")
#    con.commit()
#    con.close()

def create_purchase_table():
    con = sqlite3.connect("jer.db")
    cur = con.cursor()

    cur.execute("""
        create table sales(
            tran INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            fprice FLOAT NOT NULL,
            trev FLOAT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id));""")
    con.commit()
    con.close()


def create_products_list():
    con = sqlite3.connect("jer.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE products ( 
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT,
                    specs TEXT,
                    rev float,
                    retailprice float);''')
    reader = csv.reader(open('pro.csv', 'r'),delimiter=',')
    next(reader)
    for row in reader:
        print(row)
        to_db = [ row[1], row[2], row[3], row[4] ]
        cur.execute('''INSERT INTO products (product_name, specs, rev, retailprice)
                       VALUES ( ?, ?, ?, ?);''', to_db)
       
    con.commit()
    con.close()
    return 'pro.csv processed and data inserted into database.'
    

create_purchase_table()
create_customers_table()
create_products_list()
    
print("Successful")
   

