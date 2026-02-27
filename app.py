from model import db, Product, Media, User
from flask import jsonify   # ADD THIS AT TOP OF FILE
from flask import Flask, render_template, request, redirect, url_for, session 
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
import json
import os

app = Flask(__name__)
app.secret_key = "MB_computer_secret_key"

# -------------------------
# Configuration
# -------------------------
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')

if not os.path.isdir(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# -------------------------
# Initialize Database
# -------------------------
db.init_app(app)

with app.app_context():        
    db.create_all()

# -------------------------
# Signup Routes
@app.route('/signup', methods=['POST'])
def signup():

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    existing = User.query.filter_by(email=email).first()
    if existing:
        return "Email already registered"

    user = User(
        name=name,
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    return "Account created successfully"
# -------------------------


#login 
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session['user_id'] = user.id
            session['is_admin'] = user.is_admin

            if user.is_admin:
                return jsonify({"success": True, "redirect": "/admin"})
            else:
                return jsonify({"success": True, "redirect": "/"})

        return jsonify({"success": False})

    return render_template("Login_SignUp.html")

#about_us page 
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

#add_product.html
@app.route('/admin/add', methods=['GET', 'POST'])
def add_product():

    # ---- AUTH CHECK ----
    if 'user_id' not in session:
        return redirect(url_for('index'))

    # ---- ADMIN CHECK ----
    if not session.get('is_admin'):
        return "Unauthorized", 403

    # ---- NORMAL LOGIC ----
    if request.method == 'POST':

        name = request.form['name']
        brand = request.form['brand'].strip().title()
        #description = request.form['description']
        real_price = float(request.form['real_price'])

        old_price = request.form.get('old_price')
        old_price = float(old_price) if old_price else None

        device_type = request.form['device_type'].lower()
        discount = True if request.form.get('discount') else False
        stock = int(request.form['stock'])

        grade = request.form.get('grade')
        
        tagline = request.form.get("tagline")
        key_specs = request.form.get("key_specs")
        product_information = request.form.get("product_information")

        files = request.files.getlist('media')

        image_count = 0
        video_count = 0

        allowed_images = ('.jpg', '.jpeg', '.png', '.webp')
        allowed_videos = ('.mp4', '.mov', '.avi')

        for file in files:
            if file.filename == '':
                continue

            filename = file.filename.lower()

            if filename.endswith(allowed_images):
                image_count += 1
            elif filename.endswith(allowed_videos):
                video_count += 1
            else:
                return "Invalid file type uploaded"

        if image_count > 5:
            return "You can upload maximum 5 images"

        if video_count > 2:
            return "You can upload maximum 2 videos"

        product = Product(
         name=name,
         brand=brand,
         #description=description,
         real_price=real_price,
         old_price=old_price,
         device_type=device_type,
         discount=discount,
         stock=stock,
         tagline=tagline,
         key_specs=key_specs,
         product_information=product_information,
         grade=grade
        )
        db.session.add(product)
        db.session.commit()

        for file in files:
            if file.filename == '':
                continue

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            filetype = 'image' if filename.lower().endswith(allowed_images) else 'video'

            media = Media(
                filename=filename,
                filetype=filetype,
                product_id=product.id
            )

            db.session.add(media)

        db.session.commit()

        return redirect(url_for('admin_dashboard'))

    return render_template('add_product.html')

#admin_dashboard.html
@app.route('/admin')
def admin_dashboard():

    if not session.get("is_admin"):
        return "Access denied"

    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin_dashboard.html', products=products)

#Delete Product Route
@app.route('/admin/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):

    if 'user_id' not in session or not session.get('is_admin'):
        return "Unauthorized", 403

    product = Product.query.get_or_404(product_id)

    # Delete media files from folder
    for media in product.media:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], media.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.delete(media)

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('admin_dashboard'))

def save_file(file):
    filename = secure_filename(file.filename)
    # Add a unique prefix if you want to avoid overwriting files with the same name
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

#Edit Product Route
@app.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return "Unauthorized", 403

    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        # 1. Update Text Data
        product.name = request.form['name']
        product.brand = request.form['brand']
        product.real_price = float(request.form['real_price'])
        product.stock = int(request.form['stock'])
        product.device_type = request.form['device_type'].lower()
        product.grade = request.form.get('grade')
        product.tagline = request.form.get("tagline")
        product.key_specs = request.form.get("key_specs")
        product.product_information = request.form.get("product_information")
        product.discount = True if request.form.get('discount') else False

        # --- 1. HANDLE REMOVALS FIRST ---
        removed_files_json = request.form.get('removed_files', '[]')
        files_to_remove = json.loads(removed_files_json)
        
        for fname in files_to_remove:
            media_to_del = Media.query.filter_by(product_id=product.id, filename=fname).first()
            if media_to_del:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
                if os.path.exists(file_path):
                    os.remove(file_path)
                db.session.delete(media_to_del)
        
        # Flush deletions so the count below is accurate
        db.session.flush()

        # --- 2. VALIDATE LIMITS (5 Images, 2 Videos) ---
        new_files = request.files.getlist('media')
        allowed_images = ('.jpg', '.jpeg', '.png', '.webp')
        allowed_videos = ('.mp4', '.mov', '.avi')

        # Count what is already in the DB (after removals)
        current_images = Media.query.filter_by(product_id=product.id, filetype='image').count()
        current_videos = Media.query.filter_by(product_id=product.id, filetype='video').count()

        # Count what the admin is trying to add
        new_image_count = 0
        new_video_count = 0
        for file in new_files:
            if file and file.filename != '':
                if file.filename.lower().endswith(allowed_images):
                    new_image_count += 1
                elif file.filename.lower().endswith(allowed_videos):
                    new_video_count += 1

        if (current_images + new_image_count) > 5:
            return "Total images cannot exceed 5", 400
        if (current_videos + new_video_count) > 2:
            return "Total videos cannot exceed 2", 400

        # --- 3. SAVE NEW UPLOADS ---
        for file in new_files:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                ftype = 'image' if filename.lower().endswith(allowed_images) else 'video'
                new_media = Media(filename=filename, filetype=ftype, product_id=product.id)
                db.session.add(new_media)

        # Update other product fields
        product.name = request.form['name']
        product.brand = request.form['brand']
        product.real_price = float(request.form['real_price'])
        product.stock = int(request.form['stock'])
        # ... update other fields ...

        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_product.html', product=product)

#home page product
@app.route('/')
def home():
    products = Product.query.all()
    return render_template("home.html", products=products)

#detail page 
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("detail.html", product=product)

@app.route('/laptops')
def laptops():
    products = Product.query.filter_by(device_type="laptop").all()

    # get unique brands only from laptop
    brands = (
        db.session.query(Product.brand)
        .filter_by(device_type="laptop")
        .distinct()
        .all()
    )

    brands = [b[0] for b in brands if b[0]]

    return render_template(
        "laptop.html",
        products=products,
        brands=brands
    )

@app.route('/smartphones')
def smartphones():
    products = Product.query.filter_by(device_type="smartphone").all()

    # get unique brands only from smartphones
    brands = (
        db.session.query(Product.brand)
        .filter_by(device_type="smartphone")
        .distinct()
        .all()
    )

    brands = [b[0] for b in brands if b[0]]

    return render_template(
        "smartphone.html",
        products=products,
        brands=brands
    )

@app.route('/computers')
def computers():
    products = Product.query.filter_by(device_type="computer").all()

    # get unique brands only from computer
    brands = (
        db.session.query(Product.brand)
        .filter_by(device_type="computer")
        .distinct()
        .all()
    )

    brands = [b[0] for b in brands if b[0]]

    return render_template(
        "computer.html",
        products=products,
        brands=brands
    )

@app.route('/discount')
def discount():
    products = Product.query.filter_by(discount=True).all()

    # get unique brands only from discount
    brands = (
        db.session.query(Product.brand)
        .filter_by(discount=True)
        .distinct()
        .all()
    )

    brands = [b[0] for b in brands if b[0]]

    return render_template(
        "discount.html",
        products=products,
        brands=brands
    )
1
# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)