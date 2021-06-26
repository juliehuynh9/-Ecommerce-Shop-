from flask import Flask, render_template, jsonify, request, url_for, session, redirect
import database as db
from datetime import date, time, datetime,timedelta  
import math
import random
import string
app = Flask(__name__)
app._static_folder='static/'

app.secret_key = "super secret key"
items_cart2 = []
#IMPLEMENT INDEX PAGE
@app.route("/", methods=["GET","POST"])
def index():
    print('from index')
    if request.method == "POST":
        # IMPLEMENT SEARCH
        # if 'search' in request.form:
        key = request.form['search']
        search_products = db.retrieve_products_by_key(key)
        
        return render_template("index.html", products = search_products, login=session['login_status'], cart_item=[])
    else:
        #IF NO SEARCH KEY, DISPLAY ALL PRODUCTS
        session['all_products'] = db.retrieve_all_products()
        #view as guest
        if 'email' not in session:
            session['login_status'] = False
            return render_template("index_guest.html",products = session['all_products'])
        else:
            #view as member
            session['login_status'] = True
        return render_template("index.html",products = session['all_products'],login=session['login_status'], cart_item=[])

#IMPLEMENT SEE ORDERS HISTORY
@app.route("/previous_orders", methods=['GET', "POST"])
def previous_orders():
    orders = db.retrieve_prev_orders_from_accounts(session['email'])
    return render_template("previous_orders.html", asd=orders)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
#IMPLEMENT CHECKOUT/TRACKING
@app.route("/checkout", methods=['GET', "POST"])
def checkout():
    if request.method == 'POST':
        order_number = id_generator()
        if request.json is not None:
            shopping_cart = request.json
            for item in shopping_cart:
                item_dict = db.retrieve_products_by_name(item['name'])
                item_dict['order_number'] = order_number
                item_dict['count'] = item['count']
                item_dict['ordered_date'] = date.today().strftime("%m/%d/%Y")
                datetime_arrive = date.today() + timedelta(days=item_dict['day_to_arrive'])
                item_dict['arrived_date'] = datetime_arrive.strftime("%m/%d/%Y")
                item_dict['total'] = '$'+item['total']
                global items_cart2
                items_cart2.append(item_dict)
            session['shopping_cart'] = items_cart2
            db.add_orders_to_accounts(items_cart2, session['email'])
            # global items_cart2
            items_cart2 = []
            return render_template("checkout.html", asd=session['shopping_cart'])
    print('Update shopping cart', items_cart2)
    return render_template("checkout.html", asd=session['shopping_cart'])

#IMPLEMENT LOGOUT
@app.route("/logout", methods=["GET","POST"])
def logout():
    print('user loggout')
    if 'email' in session:
            session.pop('email', None)
    if 'shopping_cart' in session:
        session.pop('shopping_cart', None)
    session['login_status'] = False
    return redirect(url_for('index', products=session['all_products'] ))

#IMPLEMENT REGISTRATION
@app.route("/register", methods=["GET","POST"])
def register_form():
    if request.method == "POST":
        email_inp = request.form.get("email")
        password_inp = request.form.get("password")
        if len(email_inp) == 0 or len(password_inp) == 0 :
            return render_template("register.html", message="missing_info")

        email_check, password_check = db.retrieve_account(email_inp, password_inp)

        if email_check is not None:
            return render_template("register.html", message="email_exists")
        else:
            db.add_account(email_inp, password_inp)
            session['email'] = email_inp
            session['login_status'] = True
            return redirect(url_for('index', login=True))
            # return render_template("index.html")
    else:
        return render_template("register.html", message="")

#IMPLEMENT LOGIN
@app.route("/login", methods=["GET","POST"])
def login_form():
    if request.method == "POST":
        email_inp = request.form.get("email")
        password_inp = request.form.get("password")

        email_check, password_check = db.retrieve_account(email_inp, password_inp)

        if len(email_inp)==0 or len(password_inp)==0:
            return render_template("login.html", message="missing_info")
        elif email_check == email_inp and password_check == password_inp: 
            session['email'] = email_inp
            session['login_status'] = True
            print('login successfully')
            return redirect(url_for('index',products=session['all_products'] ))
        else:
            return render_template("login.html", message="failed_login")
    else:
        return render_template("login.html", message="")

#VIEW PRODUCT INFO
@app.route("/view_product/<int:id>", methods=["GET",'POST'])
def product_info(id):
    info = db.retrieve_products_by_id(id)
    ratings, reviews = db.get_ratings_reviews_by_id(id)
    ratings = str(math.floor(float(ratings)))
    #ratings and reviews LOOKS LIKE THIS:
    # ratings = 4.5/5
    # reviews = [['john', 'Good cap'], ['kelly', 'Perfect caps for a sunny day']]
    #Ex ['john', 'Good cap'] = #name of reviewer, #review

    return render_template("product_info.html", info = info, ratings=ratings, reviews=reviews)

#VIEW CONTACT INFO
@app.route("/contacts", methods=["GET"])
def contacts():
    return render_template("contacts.html")


if __name__ == '__main__':
    app.run(debug=True)