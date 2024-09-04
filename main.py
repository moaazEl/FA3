import os
from flask import Flask, flash, redirect, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "donottellanyone"

@app.route('/')
def home():
    return render_template('home.html')

def find_fprice(product_id):
    conn = sqlite3.connect('jer.db')
    cursor = conn.cursor()
    cursor.execute("select retailprice from products where product_id = ?", (product_id))
    result = cursor.fetchone()
    if result:
        fprice = result[0]  
        return fprice
    else:
        return 'NOT FOUND'

def find_trev(product_id):
    conn = sqlite3.connect('jer.db')
    cursor = conn.cursor()
    cursor.execute("select rev from products where product_id = ?", (product_id))
    result = cursor.fetchone()
    if result:
        trev = result[0]  
        return trev
    else:
        return 'NOT FOUND'

def insertcustomer(first,surname,dob,phone,email,address,password):
    con = sqlite3.connect("jer.db")
    cur = con.cursor()
    cur.execute('''INSERT INTO customers (first,surname,dob,phone,email,address,password) VALUES (?,?,?,?,?,?,?)''',
                (first,surname,dob,phone,email,address,password))
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
    cur.execute("SELECT email, password, customer_id FROM customers")
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

def retrievecustomers(email,password):
    con = sqlite3.connect("jer.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM customers where email = ? and password = ?",(email,password))
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
        password = request.form.get('password','NA')
        # Check for missing fields
        if not all([email, phone, address, first, surname, password]):
            return render_template('register.html', error_message='Please fill in All fields that are required.')

        # Check if the email already exists
        existing_customers = retrieveALLcustomers()
        for customer in existing_customers:
            if customer[0] == email:
                return render_template('register.html', error_message='Email already registered with an existing account maybe try login!!')
        print("before insert", first,surname,dob,phone,email,address,password)
        insertcustomer(first,surname,dob,phone,email,address,password)
        return render_template('register.html', success_message=f'You are registered now {first} in Cheapteck.com,  We hope we dont let you down!!', customers=customers)
        return redirect(url_for('home'))
    else:  #in get process
        return render_template('register.html',customers = customers)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error_message = None
    if request.method=='POST':
        e = request.form['email']
        c = request.form['password']
        print("e&c",e,c,)
        customers = retrievecustomers(e,c)
        if not customers:  # Check if login failed
            error_message = 'Invalid email or password. Please try again. Perhaps you dont have an account? try signing up! Please make sure you check teh box to agree to our terms and conditions.'
        else:
            return render_template('login.html', customers=customers)

    return render_template('login.html', error_message=error_message)

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
        fprice = find_fprice(selected_product_id)
        trev = find_trev(selected_product_id)
      #  formatted_date = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d-%m-%Y')
        
        conn = sqlite3.connect('jer.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sales (customer_id, product_id, date, fprice, trev) VALUES (?, ?, ?, ?, ?)", 
                       (selected_customer_id, selected_product_id, formatted_date, fprice, trev))
        tran = cursor.lastrowid

        # Update the customer record with the transaction number
        cursor.execute(''' UPDATE customers SET tran = CASE WHEN tran IS NULL OR tran = '' THEN ? ELSE tran || ',' || ? END WHERE customer_id = ?; ''', (tran, tran, selected_customer_id))
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
