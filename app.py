#routing
from flask import *
import pymysql
# create flask app
app=Flask(__name__)
# secret key
app.secret_key="fmbsmbfshjhjjh398 943*%$^#%"
@app.route('/home')
def main():
    return "This is the main page"
# CRUD
# Create
# Read
# Update
# Delete
connection=pymysql.connect(host='localhost',user='root',password='',database='sokogarden')
@app.route('/')
def getproducts():
    connection=pymysql.connect(host='localhost',user='root',password='',database='sokogarden')
#     define the sql query
    sql_phone='select * from products where prod_cat ="phones"'
    sql_others = 'select * from products where prod_cat ="others"'
#     create cursor
    phone_cursor=connection.cursor()
    others_cursor = connection.cursor()
#     use cursor to execute sql
    phone_cursor.execute(sql_phone)
    others_cursor.execute(sql_others)
#     fetch teh records
    if phone_cursor.rowcount == 0:
        return render_template("home.html",message="No products to display")
    else:
        phones=phone_cursor.fetchall()
        others = others_cursor.fetchall()
        return render_template("home.html",records=phones,others_category=others)

# single item route
@app.route("/single_item/<prod_id>")
def single_item(prod_id):
#     define the sql query to fetch product based on id
    sql='select * from products where prod_id =%s'
#     create the cursor
    cursor=connection.cursor()
    #execute the sql query
    cursor.execute(sql,prod_id)
    product=cursor.fetchone()
    return render_template("single_item.html",product=product)

# signup route
@app.route("/signup",methods=['POST','GET'])
def signup():
    if request.method =='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        confirm=request.form['confirm']
        if '@' not in email:
            return render_template("signup.html",message="Email must have '@'")
        elif password != confirm:
            return render_template("signup.html", message="Passwords do not match")
        elif len(password) <=6:
             return render_template("signup.html", message="Password must have 8 digits")
        #create the cursor
        cursor=connection.cursor()
        sql='insert into users (name,email,password) values(%s,%s,%s)'
        cursor.execute(sql,(name,email,password))
        connection.commit()
        return render_template("signup.html",message="Signup Successful")
    else:
        return render_template("signup.html")
# signin
@app.route("/signin",methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        cursor = connection.cursor()
        #     sql
        sql = 'select * from users where email=%s and password=%s'
        cursor.execute(sql, (email, password))
        session['key']=email
#         check if user exists
        if cursor.rowcount ==0:
            return render_template("signin.html",message="User does not exist")
        else:
            return render_template("signin.html",message="Signin Successful")
    else:
        return render_template("signin.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/signin')














app.run(debug=True,port=8080)

