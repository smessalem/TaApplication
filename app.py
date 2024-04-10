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

# print("debug")
# print(db.child("Products").get().val())
# for item in db.child("Products").get().val():
#     print(type(item))
#     print(db.child("Products").get().val()[item]['name'])


# db.child("Users").set("UID")
# p9 = {"name": "Webcam", "price": "50", "src": "p9.png"}
# db.child('Products').child("p9").set(p9)
@app.route('/home')
def home():
    UID = login_session['user']['localId']
    return render_template("index.html", name=db.child("Users").child(UID).child('name').get().val(),
                           db_products=db.child("Products").get().val(), uid=UID)

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
                    db.child("Users").child(login_session['user']['localId']).child("Cart").set("product_id")
                    return redirect(url_for('home', name=username))
                except:
                    error = "Email already in use | Password less than 6 characters"
                    return redirect(url_for('error', error_msg=error))
            else:
                error = "Confirm password does not match password"
                return redirect(url_for('error', error_msg=error))
        except Exception as e:
                print(f"There was an error: {e}")
                error = "There was an error"
                return redirect(url_for('error', error_msg=error))
    else:
        return render_template('signup.html')


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    print("Sign Out Successful")
    return redirect(url_for('signup'))

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product')
def product():
    return render_template('product.html', db_products=db.child("Products").get().val())

@app.route('/why')
def why():
    return render_template('why.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/add_to_cart/<string:item>', methods=['GET', 'POST'])
def add_to_cart(item):
    print("debug")
    UID = login_session['user']['localId']
    db.child('Users').child(UID).child('Cart').child('cart').push(item)
    print("debug2")
    return redirect(url_for('home'))

@app.route('/remove_cart/<string:item>', methods=['GET', 'POST'])
#TODO: add cart removal

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    uid = login_session['user']['localId']
    my_cart = db.child('Users').child(uid).child('Cart').child('cart').get().val()
    my_products = db.child("Products").get().val()
    cart_total = 0
    if not (my_cart == None):
        for item in my_cart:
            cart_total += int(my_products[my_cart[item]]['price'])

    return render_template('cart.html', cart=my_cart,
                           db_products=my_products, total=cart_total)

@app.route('/account')
def account():
    UID = login_session['user']['localId']
    return render_template('account.html', name=db.child("Users").child(UID).child('name').get().val(),
                           email=db.child("Users").child(UID).child('email').get().val())

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    app.secret_key = 'If monkeys can write Shakespeare, they can write this too.'
    app.run()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
