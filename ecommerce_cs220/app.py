from flask import Flask, render_template, jsonify, request, url_for, session, redirect
# from flask_session import Session
import login


app = Flask(__name__)

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"



@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        if request.form['action'] == "register":
            username_inp = request.form.get("username_reg")
            password_inp = request.form.get("password_reg")
            address_inp = request.form.get("address_reg")

            if username_inp == None or password_inp == None or address_inp == None:
                return render_template("error.html", message="Must enter all fields.")

            username_check, password_check = login.retrieve_account(username_inp, password_inp)

            if username_check is not None:
                return render_template("error.html", message="Username already exists.")
            else:

                login.add_account(username_inp, password_inp, address_inp)
                return render_template("success.html", message="Registration success.")
        else: #action = "login"
            username_inp = request.form.get("username_login")
            password_inp = request.form.get("password_login")

            username_check, password_check = login.retrieve_account(username_inp, password_inp)

            if username_inp is None or password_inp is None:
                return render_template("error.html", message="Must enter all fields")

            if username_check is None or password_check is None:
                return render_template("status.html", message="Error retriving account.")
            if username_check == username_inp and password_check == password_inp: 
                message = username_inp + " log in successfully "
                
                return render_template("status.html", message=message)
            else:
                return render_template("status.html", message="Username and password does not match.")
    else:
        return render_template("index2.html")

if __name__ == '__main__':
    app.run(debug=True)