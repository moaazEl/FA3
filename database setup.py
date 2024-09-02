import csv, sqlite3,os

if os.path.isfile("jer.db"):
    os.remove('jer.db')

def create_customers_table():
    con = sqlite3.connect("jer.db")
    cur = con.cursor()

    cur.execute("""
        create table customers (
        customer_id integer primary key autoincrement,
        address text not null,
        first text not null,
        surname text not null,
        phone text not null,
        dob text,
        tran integer,
        email text not null
        );""")
    reader = csv.reader(open('cus.csv', 'r'),delimiter=',')
    next(reader)
    for row in reader:
        print(row)
        to_db = [ row[1], row[2], row[3], row[7], row[4], row[5], row[6]]
        cur.execute('''INSERT INTO customers (first, surname, dob, email, phone, address, tran)
                       VALUES ( ?, ?, ?, ?, ?, ?, ?);''', to_db)
       
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
        tran integer primary key autoincrement,
        customer_id integer not null,
        product_id integer not null,
        date text not null,
        fprice float not null,
        trev float not null);""")
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
   

