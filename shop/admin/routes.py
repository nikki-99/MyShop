from flask import render_template, session, redirect, request, url_for, flash
from shop import app, db, bcrypt
from .forms import RegistrationForm,LoginForm
from .models import User
from shop.products.models import Addproduct
from shop.customers.models import Order, Customer



@app.route('/admin')

def admin():
    if 'email' not in session:
        flash(f'Login first','danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()    
    return render_template('admin/index.html', title = 'Admin', products = products)






@app.route('/register', methods = ['GET','POST'])
def register():

    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name = form.name.data, email = form.email.data, password = hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome { form.name.data }.Thank you for registering! Now you are able to login','success')
        return redirect(url_for('login'))

    return render_template('admin/register.html', form = form , title = 'Register')


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data

            flash(f'Welcome { form.email.data }. You are now logged in!','success')
            return redirect(url_for('admin'))
        elif user is None:
            flash(f'You are not a registered as a Admin. Registered yourself first!', 'danger')                 
        else:
            flash(f'Wrong password or email. Please try again', 'danger')    
    return render_template('admin/login.html',form = form, title = 'Login Page')    


@app.route('/admin_shop')
def admin_shop():
    page = request.args.get('page',1,type = int)
    order = Order.query.all()
    products = Addproduct.query.filter(Addproduct.stock>0).paginate(page = page,per_page = 4)
    #  brand whose any time doesn't exist no need to show
    

    return render_template('admin/shop.html', products = products, title = 'Home', order = order)




@app.route('/detail')
def detail():
    order = Order.query.all()
    customer = Customer.query.all()
    return render_template('admin/detail.html', order=order, customer = customer)    

       