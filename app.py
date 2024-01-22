from flask import Flask, render_template, url_for, request, redirect, flash, session
from Forms import RegistrationForm, LoginForm, DeleteUserForm
from customer_login import CustomerLogin, RegisterCustomer, DeleteCustomer
from customer import Customer
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
import shelve

app = Flask(__name__)


app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):        
    with shelve.open('userdb', 'c') as userdb:
        for keys in userdb:
            if keys == id:
                return userdb[id]

login_manager.init_app(app)

#home page
@app.route('/')
def home():
    return render_template('home.html')

#order page
@app.route('/order')
def order():
    return render_template('order.html')


#About us pages
@app.route('/openingHours')
def openingHours():
    return render_template('openingHours.html')

@app.route('/findUs')
def findUs():
    return render_template('findUs.html')

@app.route('/contactUs')
def contactUs():
    return render_template('contactUs.html')

#Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('userdb', 'c') as userdb:
            user = CustomerLogin(form.phoneNumber.data, form.password.data)
            if isinstance(user, Customer):
                for keys in userdb:
                    if user.get_id() == keys:
                        if form.remember.data == True:
                            login_user(user, remember=True)
                            session['id'] = user.get_id()
                            return redirect('/home')
                        login_user(user)
                        session['id'] = user.get_id()
                        return redirect('/home')

            else:
                flash("wrong username/password. please try again")
                return redirect(url_for('login'))
    return render_template('login.html', form=form)

#Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('userdb', 'c') as userdb:
            if str(form.phoneNumber.data) not in userdb:
                user = RegisterCustomer(form.name.data, form.phoneNumber.data, form.password.data, form.gender.data, form.securityQuestion.data, form.securityAnswer.data)
                if isinstance(user, Customer):
                    userdb[user.get_id()] = user
                    flash('Registration Successful!', "success")
                    return redirect(url_for('login'))
            else:
                flash("Already registered please login instead" , 'success')
                return redirect(url_for('login'))
    return render_template('register.html', form=form)

#edit page
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('userdb', 'c') as userdb:
            user = RegisterCustomer(form.name.data, form.phoneNumber.data, form.password.data, form.gender.data, form.securityQuestion.data, form.securityAnswer.data)
            if isinstance(user, Customer):
                userdb[str(user.get_id())] = user
                flash('Successfully edited')
            else:
                flash('Edit not successful')

    return render_template('edit.html', form=form)


#delete users page
@app.route('/deleteUser', methods=['GET', 'POST'])
def deleteUsers():
    form = DeleteUserForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('userdb', 'c') as userdb:
            user = DeleteCustomer(form.phoneNumber.data, form.password.data)
            if isinstance(user, Customer):
                count = 0
                for keys in userdb:
                    count += 1
                    if keys == user.get_id():
                        del(userdb[user.get_id()])
                        flash('Successfully deleted')

                    if count == len(userdb):
                        flash('delete not successful')
            

    return render_template('deleteUser.html', form=form)


@app.route('/dbCheck')
@login_required
def dbCheck():
    user_list = []
    with shelve.open('userdb', 'c') as userdb:
        if len(userdb) == 0:
            raise 404

        else:
            for key in userdb:
                if key == session['id']:
                    print(userdb[key])

    return render_template("dbCheck.html", user_list=user_list)

#Logout 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('id')
    flash("User successfully logged out." , 'success')
    return redirect(url_for("home"))


#Error handling
@app.errorhandler(401)
def not_authorised(error):
        return render_template('error.html', error_code = 401, message = "Please login to view this page")
    
@app.errorhandler(404)
def not_found(error):
        return render_template('error.html', error_code = 404, message = 'Page not found. Sorry for the inconvinience caused.')
    
@app.errorhandler(500)
def unknown_error(error):
        return render_template('error.html', error_code = 500, message='Unknown error occured')
    


if __name__ == '__main__':
    app.run(debug = True)