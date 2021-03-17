from flask import render_template, session, redirect, request, url_for, flash, current_app
from shop import app, db, photos 
from .models import Addproduct
from .forms import Addproducts
import secrets, os






@app.route('/home')
def home():
    page = request.args.get('page',1,type = int)
    q = request.args.get('q')

    if q:
        products = Addproduct.query.filter(Addproduct.name.contains(q)).paginate(page = page, per_page=4)
    else:
      
        products = Addproduct.query.filter(Addproduct.stock>0).paginate(page = page,per_page = 4)
    #  brand whose any time doesn't exist no need to show
    

    return render_template('products/index.html', products = products,  title = 'Home')

@app.route('/product/<int:id>')
def description(id):
    product = Addproduct.query.get_or_404(id)

    return render_template('products/description.html', product = product,  title = 'Description')











 




 




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


