from flask import render_template, session, redirect, request, url_for, flash, current_app
from shop import app, db, photos, bcrypt, login_manager
from .forms import CustomerRegistrationForm, CustomerLoginForm
from .models import Customer
from flask_login import login_user, current_user,login_required, logout_user
import secrets, os



@app.route('/customer/register', methods=['GET','POST'])
def customer_registration():
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Customer(name = form.name.data, username = form.username.data, email = form.email.data, password= hashed_password,country = form.country.data,\
            state = form.state.data,city = form.city.data,address = form.address.data,pin = form.pincode.data,contact = form.contact.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Thank you for regestering!  You are now able to log in!', 'success')
        return redirect(url_for('customer_login')) 
    return render_template('customer/register.html',title = 'Register', form = form)  


@app.route('/customer/login', methods=['GET','POST']) 
def customer_login():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            
            return redirect(url_for('home'))
        else:    
            
            flash(f'Login Unsuccessful. Please check email or password','danger')
            return redirect(url_for('customer_login'))
    return render_template('customer/login.html',title = 'Login', form = form)            


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))    