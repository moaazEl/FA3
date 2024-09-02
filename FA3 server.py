from flask import Flask
from flask import Flask, flash, redirect, render_template, request, redirect,url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "donottellanyone"

@app.route('/')
def home():
     return render_template('home.html')


def insertcustomer(first,surname,dob,phone,email,address):
    con = sqlite3.connect("jer.db")
    cur = con.cursor()
    cur.execute('''INSERT INTO customers (first,surname,dob,phone,email,address) VALUES (?,?,?,?,?,?)''',
                (first,surname,dob,phone,email,address))
    con.commit()
    con.close()

def insertproduct(product_name, specs, rev, retailprice):
    con = sqlite3.connect("jer.db")
    cur = con.cursor()
    cur.execute('''INSERT INTO products (product_name, specs, rev, retailprice) VALUES (?,?,?,?)''',
                (product_name, specs, rev, retailprice))
    con.commit()
    con.close()

def retrieveALLcustomers():
    con = sqlite3.connect("jer.db")
    cur = con.cursor()
    cur.execute("SELECT email, customer_id FROM customers")
    customers = cur.fetchall()
    con.close()
    return customers

def retrieveALLproducts():
    con = sqlite3.connect("jer.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    con.close()
    return products

def retrievecustomers(email,customer_id):
    con = sqlite3.connect("jer.db")
    cur = con.cursor()
    cur.execute("SELECT email, customer_id FROM customers where email = ? and customer_id = ?",(email,customer_id))
#look at https://digisoln.com/flask/flask/SQLiteExamples
    customers = cur.fetchall()
    print("customers", customers)
    con.close()
    return customers
  
@app.route('/register', methods=['POST', 'GET'])
def register():
    print(request.method)
    customers = retrieveALLcustomers()
    print("customers",customers)
    if request.method =='POST':
        email = request.form.get('email','NA')
        phone = request.form.get('phone','NA')
        address = request.form.get('address','NA')
        dob = request.form.get('dob','NA')
        first = request.form.get('first','NA')
        surname = request.form.get('surname','NA')
        print("before insert", first,surname,dob,phone,email,address)
        insertcustomer(first,surname,dob,phone,email,address)
        return render_template('register.html', customers=customers)
        return redirect(url_for('home'))
    else:  #in get process
        return render_template('register.html',customers = customers)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        e = request.form['email']
        c = request.form['customer_id']
        print("e&c",e,c,)
        customers = retrievecustomers(e,c)
        return render_template('login.html', customers=customers)
    else: #in get process
        return render_template('login.html')

@app.route('/products')
def display_products():
    conn = sqlite3.connect("jer.db")
    cursor = conn.cursor()
    sql = ''' SELECT product_id, product_name, specs, retailprice FROM products''';
    cursor.execute(sql)
    products_data = cursor.fetchall()
    return render_template("products.html", products_data = products_data) 

@app.route('/display_customers')
def display_customers():
    conn = sqlite3.connect("jer.db")
    cursor = conn.cursor()
    sql = ''' SELECT * FROM customers''';
    cursor.execute(sql)
    customers_data = cursor.fetchall()
    return render_template("customers.html", customers_data = customers_data)

@app.route('/insert_product', methods=['POST', 'GET'])
def insert_product():
    print(request.method)
    products = retrieveALLproducts()
    print("products",products)
    if request.method =='POST':
        product_name = request.form.get('product_name')
        specs = request.form.get('specs','NA')
        rev = request.form.get('rev','NA')
        retailprice = request.form.get('retailprice','NA')
        print("before insert", product_name, specs, rev, retailprice)
        insertproduct(product_name, specs, rev, retailprice)
        return render_template('new_products.html', products=products)
        return redirect(url_for('home'))
    else:  #in get process
        return render_template('new_products.html',products = products)

#Function to get customer data from the database
def get_customers():
    conn = sqlite3.connect('jer.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()
    conn.close()
    return data

# Function to get products data from the database
def get_products():
    conn = sqlite3.connect('jer.db')
    cursor = conn.cursor()
    cursor.execute("select * FROM products")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/add_sales',methods=['POST','GET'])
def add_sales():
    print("add_salesmethods being used:",request.method)
    if request.method=='GET':
        customers = get_customers();
        print(customers)
        products = get_products();   
        print(products)
        return render_template('add_sales.html', customers=customers, products=products)
    else:
        selected_customer_id = request.form['customer']
        selected_product_id = request.form['product'] 
        selected_date = request.form['date']
        fprice = request.form['fprice']
        trev = request.form['trev']
      #  formatted_date = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d-%m-%Y')
        
        conn = sqlite3.connect('jer.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sales (customer_id, product_id, date, fprice, trev) VALUES (?, ?, ?, ?, ?)", 
                       (selected_customer_id, selected_product_id, formatted_date, fprice, trev))
        conn.commit()
        conn.close() 
    return redirect(url_for('display_sales'))

# Function to get data from the salesdata
def get_sales():
    conn = sqlite3.connect('jer.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM sales
    ''')
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/display_sales')
def display_sales():
    salesdata = get_sales()
    print(salesdata)
    return render_template('display_sales.html', salesdata=salesdata)


if __name__ == "__main__":
    app.run()
