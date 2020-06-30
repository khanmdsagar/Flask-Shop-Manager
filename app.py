import os
import secrets
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from PIL import Image



UPLOAD_FOLDER = 'static/files'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '5453get34wfgs423'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

class items(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    price = db.Column(db.String(200), nullable = False)
    quantity = db.Column(db.String(200), nullable = False)
    photoPath = db.Column(db.String(200), nullable = False)
    
    def __init__(self, name, price, quantity, photoPath):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.photoPath = photoPath



#index page
@app.route('/')
def index():
    page = request.args.get('page', 1, type = int)
    allItems = items.query.order_by(items.id.desc()).paginate(page = page, per_page = 5)
    return render_template('index.html', allItems = allItems)


#go to insert page
@app.route('/insert-page')
def insert():
    return render_template('insert.html')


#go to update page
@app.route('/update-page/<string:id>')
def update(id):
    results = items.query.filter(items.id == id).all()
    return render_template('update.html', results = results)


#update operation
@app.route('/updateOperation/<string:id>')
def updateOperation(id):
    return render_template('update.html', id = id)


@app.route('/confirm_delete/<string:id>')
def confirm_delete(id):
    return render_template('confirm_delete.html', id = id)


@app.route('/delete/<string:id>', methods = ['POST'])
def delete(id):
    id = items.query.get_or_404(id)
    item = self.session.query(Item).get(id)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.filename))

    db.session.delete(id)
    db.session.commit()
    flash('Item has Deleted')
    return redirect(url_for('index'))


@app.route('/uploadFile', methods = ['GET', 'POST'])
def uploadFile():

    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename) 

        token = secrets.token_hex(8)
        newFileName = str(token) + filename
        
        filepath = 'files/' + newFileName
       
        if filename == '':
            flash('No selected file')
            return redirect(url_for('insert'))

        elif (filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS):
            flash('File not allowed')
            return redirect(url_for('insert'))


        elif (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):

            item = items(request.form['name'], request.form['price'], request.form['quantity'], filepath)
            
            db.session.add(item)
            db.session.commit()
         
            output_size = (100, 100)
            i = Image.open(file)
            i.thumbnail(output_size)
            i.save(os.path.join(app.config['UPLOAD_FOLDER'], newFileName))

            flash('Record added successfully')
            return redirect(url_for('insert'))

        else:
            flash('File upload failed')
            return redirect(url_for('insert'))


if __name__ == "__main__":
    app.run(debug = True)
