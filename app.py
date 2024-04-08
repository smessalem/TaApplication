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
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config);
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')

# db.child("Users").set("UID")
@app.route('/home')
def home():
    UID = login_session['user']['localId']
    return render_template("home.html", name=db.child("Users").child(UID).child('name').get().val())

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['signin-email']
        password = request.form['signin-password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return redirect(url_for('signup', error_msg=error))

@app.route('/', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        username = request.form['signup-fullname']
        email = request.form['signup-email']
        password = request.form['signup-password']
        confirm_password = request.form["signup-confirm_password"]
        try:
            if password == confirm_password:
                try:
                    login_session['user'] = auth.create_user_with_email_and_password(email, password)
                    UID = login_session['user']['localId']
                    user = {"email" : email, "password" : password, "name" : username}
                    db.child("Users").child(UID).set(user)
                    return redirect(url_for('home', name=username))
                except:
                    return render_template("error.html", error="Email already in use")
            else:
                return render_template("signup.html", error="Confirm password does not match password")
        except Exception as e:
                print(f"There was an error: {e}")
                return render_template("signup.html", error="There was an error")
    else:
        return render_template('signup.html')


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
