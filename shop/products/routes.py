from flask import render_template, session, redirect, request, url_for, flash
from shop import app, db, photos 
from .models import Brand, Category,Addproduct
from .forms import Addproducts
import secrets




@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Login first','danger')
        return redirect(url_for('login'))
    if request.method =='POST':
        getbrand =request.form.get('brand')
        brand = Brand(name = getbrand)
        db.session.add(brand)
        db.session.commit()
        flash(f'The Brand {getbrand} is added','success')
        return redirect(url_for('addbrand'))

    return render_template('products/addbrand.html', brands = 'brands')
 
@app.route('/updatebrand/<int:id>', methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Login first','danger')
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =='POST':
        updatebrand.name = brand
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))    

    return render_template('products/updatebrand.html',title = 'Update Brand', updatebrand = updatebrand)



@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'Login first','danger')
        return redirect(url_for('login'))
    if request.method =='POST':
        getcat =request.form.get('category')
        cat = Category(name = getcat)
        db.session.add(cat)
        db.session.commit()
        flash(f'The Category {getcat} is added','success')
        return redirect(url_for('addcat'))

    return render_template('products/addbrand.html')
 
@app.route('/updatecat/<int:id>', methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Login first','danger')
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method =='POST':
        updatecat.name = category
        flash(f'Your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('category'))    

    return render_template('products/updatebrand.html',title = 'Update Category', updatecat = updatecat)


@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts()
    if request.method =='POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        description = form.description.data
        # this two are not in the form 
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'),name = secrets.token_hex(10)+ ".")
        image_2=photos.save(request.files.get('image_2'),name = secrets.token_hex(10)+ ".")
        image_3=photos.save(request.files.get('image_3'),name = secrets.token_hex(10)+ ".")
        addproduct = Addproduct(name = name,price = price,discount = discount, stock = stock, colors=colors, description = description, brand_id = brand, category_id = category, image_1 = image_1, image_2=image_2, image_3=image_3)
        db.session.add(addproduct)
        db.session.commit()
        flash(f'The product { name } has been added!','success')
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form = form, title = 'Add Product', brands = brands, categories= categories)



@app.route('/updateproduct/<int:id>', methods =['GET','POST'])    
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    
    form = Addproducts()
    if request.method =='POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.description = form.description.data
        db.session.commit()
        flash(f'Your product has been updated','success')
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    
    form.colors.data= product.colors
    form.description.data=product.description
    return render_template('products/updateproduct.html', form = form, brands=brands, categories= categories, product = product)
