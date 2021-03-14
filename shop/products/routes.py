from flask import render_template, session, redirect, request, url_for, flash, current_app
from shop import app, db, photos 
from .models import Brand, Category,Addproduct
from .forms import Addproducts
import secrets, os



def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories



@app.route('/home')
def home():
    page = request.args.get('page',1,type = int)
    products = Addproduct.query.filter(Addproduct.stock>0).paginate(page = page,per_page = 4)
    #  brand whose any time doesn't exist no need to show
    

    return render_template('products/index.html', products = products, brands = brands(),categories=categories(), title = 'Home')

@app.route('/product/<int:id>')
def description(id):
    product = Addproduct.query.get_or_404(id)

    return render_template('products/description.html', product = product, brands = brands(), categories = categories(), title = 'Description')



@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page',1,type = int)
    page_brand = Brand.query.filter_by(id=id).first_or_404()
    brand_pro = Addproduct.query.filter_by(brand = page_brand).paginate(page = page,per_page = 4)


    return render_template('products/index.html', brand_pro = brand_pro, brands = brands(),categories=categories(), page_brand= page_brand, title='Home(brand)')   





@app.route('/category/<int:id>')
def get_cat(id):
    page = request.args.get('page',1,type = int)
    page_cat = Category.query.filter_by(id=id).first_or_404()
    category_pro = Addproduct.query.filter_by(category= page_cat).paginate(page = page,per_page = 4)
  
    return render_template('products/index.html',category_pro = category_pro, categories=categories(), brands = brands(), page_cat = page_cat, title = 'Home(category)')




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


@app.route('/deletebrand/<int:id>', methods = ['POST'])
def deletebrand(id):

    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand { brand.name} has been deleted','success')

        return redirect(url_for('admin'))
    flash(f'{brand.name} can not  be deleted','warning')   
    return redirect(url_for('admin')) 


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


@app.route('/deletecat/<int:id>', methods = ['POST'])
def deletecat(id):

    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category { category.name} has been deleted','success')

        return redirect(url_for('admin'))
    flash(f'{category.name} can not  be deleted','warning')   
    return redirect(url_for('admin')) 


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
       
        description = form.description.data
        # this two are not in the form 
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'),name = secrets.token_hex(10)+ ".")
        image_2 = photos.save(request.files.get('image_2'),name = secrets.token_hex(10)+ ".")
        image_3 = photos.save(request.files.get('image_3'),name = secrets.token_hex(10)+ ".")
        image_4 = photos.save(request.files.get('image_4'),name = secrets.token_hex(10)+ ".")
       
        addproduct = Addproduct(name = name,price = price,discount = discount, stock = stock, description = description, brand_id = brand, category_id = category, image_1 = image_1, image_2=image_2,image_3 = image_3, image_4=image_4)
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
    return render_template('products/updateproduct.html', form = form, brands=brands, categories= categories, product = product)



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


