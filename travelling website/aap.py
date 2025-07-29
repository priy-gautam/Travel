from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'topsecret!'

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'priya@123_0',
    'database': 'travel',
}

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Simple DB connection function
def get_db():
    return pymysql.connect(**db_config)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/destination')
def destination():
    return render_template('destination.html')

@app.route('/tour')
def tour():
    return render_template('tour.html')

@app.route('/book', methods=['GET', 'POST'])

def book():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        destination = request.form.get('destination')
        date = request.form.get('date')
        notes = request.form.get('notes')
        payment_proof = request.files.get('payment-proof')

        filename = ''
        if payment_proof and allowed_file(payment_proof.filename):
            filename = secure_filename(payment_proof.filename)
            payment_proof.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        elif payment_proof and payment_proof.filename != '':
            flash("Invalid file type.")
            return redirect(request.url)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bookings (name, email, phone, destination, travel_date, notes, payment_proof) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, email, phone, destination, date, notes, filename)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('submitted'))

    return render_template('book.html')

@app.route('/submitted')
def submitted():
    return render_template('submitted.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (name, email, phone, message) VALUES (%s, %s, %s, %s)",
            (name, email, phone, message)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('send'))  # <-- use endpoint name, not template filename
    return render_template('contact.html')

@app.route('/send')
def send():
    return render_template('send.html')  # your thank you page template






if __name__ == '__main__':
    app.run(debug=True)
