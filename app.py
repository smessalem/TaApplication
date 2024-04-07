from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase


# Your web app's Firebase configuration
config = {
  "apiKey": "AIzaSyBP4L6LTVZzV3n-Aff3o6C0OVQt6cCC1KM",
  "authDomain": "ta-application-cf857.firebaseapp.com",
  "projectId": "ta-application-cf857",
  "storageBucket": "ta-application-cf857.appspot.com",
  "messagingSenderId": "207116901642",
  "appId": "1:207116901642:web:cb95884028e3f8d3aaeef3",
  "databaseURL": "https://ta-application-cf857-default-rtdb.europe-west1.firebasedatabase.app/",
};

# Initialize Firebase
firebase = pyrebase.initialize_app(config);
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    return render_template("home.html")
# @app.route('/signup', methods=['POST', 'GET'])
# def signup():
#     if request.method == 'POST':
#         email = request.form["email"]
#         password = request.form["password"]
#         confirm_password = request.form["confirm_password"]
#         try:
#             if password == confirm_password:
#                 try:
#                     login_session['user'] = auth.create_user_with_email_and_password(email, password)
#                     user = {"email" : email, "password" : password}
#                     db.child("Users").child(login_session['user']['localId']).set(user)
#                     db.child("Users").child(login_session['user']['localId']).child("Cart").set({"setup" : "cart"})
#
#                     return render_template("signin.html")
#                 except:
#                     return render_template("signin.html", error="Email already in use")
#             else:
#                 return render_template("signin.html", error="Confirm password does not match password")
#         except Exception as e:
#             print(f"There was an error: {e}")
#             return render_template("signin.html", error="There was an error")
#     else:
#         return render_template('signin.html')
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.log_in_user_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        username = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form["confirm_password"]
        try:
            if password == confirm_password:
                try:
                    login_session['user'] = auth.create_user_with_email_and_password(email, password)
                    user = {"email" : email, "password" : password, "name" : username}
                    db.child("Users").child(login_session['user']['localId']).set(user)
                    return redirect(url_for('home'))
                except:
                    return render_template("signin.html", error="Email already in use")
            else:
                return render_template("signin.html", error="Confirm password does not match password")
        except Exception as e:
                print(f"There was an error: {e}")
                return render_template("signin.html", error="There was an error")
    else:
        return render_template('signin.html')


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    app.run()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
