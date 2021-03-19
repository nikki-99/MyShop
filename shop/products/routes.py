from flask import render_template, session, redirect, request, url_for, flash, current_app
from shop import app, db, photos 
from .models import Addproduct, Review
from .forms import Addproducts, ReviewForm 
import secrets, os
from flask_login import login_user, current_user,login_required, logout_user







@app.route('/home')
def home():
    page = request.args.get('page',1,type = int)
    q = request.args.get('q')

    if q:
        products = Addproduct.query.filter(Addproduct.name.contains(q)).paginate(page = page, per_page=4)
    else:
      
        products = Addproduct.query.filter(Addproduct.stock>0).paginate(page = page,per_page = 4)
    
    

    return render_template('products/index.html', products = products,  title = 'Home')




@app.route('/product/<int:id>', methods = ['GET', 'POST'])
@login_required
def description(id):
    page = request.args.get('page',1,type = int)
    product = Addproduct.query.get_or_404(id)
    form = ReviewForm()
    if request.method == 'POST':
        if form.validate_on_submit() :
            if form.username.data != current_user.username:
                flash(f'Please enter your own username', 'danger')
            else:    
                
                review = Review(username = form.username.data, body = form.body.data,rating = form.rating.data, product_id = id)
                db.session.add(review)
                db.session.commit()
                flash(f'Your review has been posted..Thank You!','success')
                return redirect(url_for('description', id = id)) 
               
    
    
        
    reviews = Review.query.filter_by(product_id= id).paginate(page = page, per_page=4)   

    return render_template('products/description.html', product = product,  title = 'Description',  reviews = reviews, form = form)




    





 




 




@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Login first','danger')
        return redirect(url_for('login'))
  
    form = Addproducts()
    if request.method =='POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
       
        description = form.description.data
        # this two are not in the form 
     
        image_1 = photos.save(request.files.get('image_1'),name = secrets.token_hex(10)+ ".")
        image_2 = photos.save(request.files.get('image_2'),name = secrets.token_hex(10)+ ".")
        image_3 = photos.save(request.files.get('image_3'),name = secrets.token_hex(10)+ ".")
        image_4 = photos.save(request.files.get('image_4'),name = secrets.token_hex(10)+ ".")
       
        addproduct = Addproduct(name = name,price = price,discount = discount, stock = stock, description = description, image_1 = image_1, image_2=image_2,image_3 = image_3, image_4=image_4)
        db.session.add(addproduct)
        db.session.commit()
        flash(f'The product { name } has been added!','success')
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form = form, title = 'Add Product')



@app.route('/updateproduct/<int:id>', methods =['GET','POST'])    
def updateproduct(id):
   
    product = Addproduct.query.get_or_404(id)

    
    form = Addproducts()
    if request.method =='POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
       
      
        product.description = form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/"+ product.image_1))
                product.image_1 = iphotos.save(request.files.get('image_1'),name = secrets.token_hex(10)+ ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'),name = secrets.token_hex(10)+ ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/"+ product.image_2))
                product.image_2 = iphotos.save(request.files.get('image_2'),name = secrets.token_hex(10)+ ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'),name = secrets.token_hex(10)+ ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/"+ product.image_3))
                product.image_3 = iphotos.save(request.files.get('image_3'),name = secrets.token_hex(10)+ ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'),name = secrets.token_hex(10)+ ".")
        if request.files.get('image_4'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/"+ product.image_4))
                product.image_4 = iphotos.save(request.files.get('image_4'),name = secrets.token_hex(10)+ ".")
            except:
                product.image_4 = photos.save(request.files.get('image_4'),name = secrets.token_hex(10)+ ".")                                                
        
        db.session.commit()
        flash(f'Your product has been updated','success')
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    
  
    form.description.data=product.description
    return render_template('products/updateproduct.html', form = form,  product = product)



@app.route('/deleteproduct/<int:id>', methods = ['POST'])
def deleteproduct(id):

    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/"+ product.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/images/"+ product.image_2))
                os.unlink(os.path.join(current_app.root_path, "static/images/"+ product.image_3))
                os.unlink(os.path.join(current_app.root_path, "static/images/"+ product.image_4))
 
               
            except Exception as e:
                print(e)    

        db.session.delete(product)
        db.session.commit()
        flash(f'The product { product.name} has been deleted','success')

        return redirect(url_for('admin'))
    flash(f'{product.name} can not  be deleted','warning')   
    return redirect(url_for('admin')) 



