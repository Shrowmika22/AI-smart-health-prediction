from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Simple in-memory user store with roles
users = {}  # format: {username: {"password": hashed_pw, "role": "Patient/Doctor/Admin"}}

# --------- REGISTER ---------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if username in users:
            flash("Username already exists!")
            return redirect(url_for('register'))

        users[username] = {
            "password": generate_password_hash(password),
            "role": role
        }
        flash(f"Registration successful as {role}! Please login.")
        return redirect(url_for('login'))
    return render_template("register.html")

# --------- LOGIN ---------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if username in users:
            stored_user = users[username]
            if check_password_hash(stored_user['password'], password) and stored_user['role'] == role:
                session['username'] = username
                session['role'] = role
                flash(f"Login successful as {role}!")
                return redirect(url_for('home'))
            else:
                flash("Invalid password or role!")
                return redirect(url_for('login'))
        else:
            flash("Username does not exist!")
            return redirect(url_for('login'))

    return render_template("login.html")

# --------- LOGOUT ---------
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash("Logged out successfully!")
    return redirect(url_for('login'))

# --------- HOME ---------
@app.route('/')
def home():
    if 'username' in session:
        return render_template("index.html", username=session['username'], role=session['role'])
    else:
        return redirect(url_for('login'))

# --------- PREDICT ---------
@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        flash("Please login first!")
        return redirect(url_for('login'))

    symptoms = request.form.getlist('symptoms')

    # Initialize empty lists
    diseases_found = []
    all_home_remedies = []
    all_medicines = []

    # ---- Check all diseases ----
    if "fever" in symptoms or "cold" in symptoms or "cough" in symptoms:
        diseases_found.append("Common Cold")
        all_home_remedies.extend([
            {"name": "Drink warm water with lemon", "image": "lemon_water.jpg"},
            {"name": "Breathing exercises", "image": "breathing.jpg"}
        ])
        all_medicines.extend([
            {"name": "Paracetamol", "image": "paracetamol.jpg"},
            {"name": "Vitamin C", "image": "vitamin_c.jpg"}
        ])

    if "body pains" in symptoms or "headache" in symptoms:
        diseases_found.append("Flu")
        all_home_remedies.extend([
            {"name": "Take rest", "image": "rest.jpg"},
            {"name": "Warm compress", "image": "warm_compress.jpg"}
        ])
        all_medicines.extend([
            {"name": "Paracetamol", "image": "paracetamol.jpg"},
            {"name": "Consult doctor", "image": "doctor.jpg"}
        ])

    if "chest pain" in symptoms or "breathing difficulty" in symptoms:
        diseases_found.append("Heart Disease")
        all_home_remedies.extend([
            {"name": "Avoid heavy exercise", "image": "exercise.jpg"},
            {"name": "Reduce stress", "image": "meditation.jpg"}
        ])
        all_medicines.extend([
            {"name": "Consult cardiologist", "image": "doctor.jpg"}
        ])

    if "diabetes" in symptoms:
        diseases_found.append("Diabetes")
        all_home_remedies.extend([
            {"name": "Exercise regularly", "image": "exercise.jpg"},
            {"name": "Control sugar intake", "image": "healthy_food.jpg"}
        ])
        all_medicines.extend([
            {"name": "Insulin / Medicine as prescribed", "image": "medicine.jpg"}
        ])

    if "skin rash / itching" in symptoms:
        diseases_found.append("Skin Allergy")
        all_home_remedies.extend([
            {"name": "Use mild soap", "image": "soap.jpg"},
            {"name": "Apply aloe vera", "image": "aloe_vera.jpg"}
        ])
        all_medicines.extend([
            {"name": "Anti-allergy cream", "image": "cream.jpg"}
        ])

    if "period pain" in symptoms:
        diseases_found.append("Menstrual Cramps")
        all_home_remedies.extend([
            {"name": "Hot water bag", "image": "hot_water_bag.jpg"},
            {"name": "Light exercises", "image": "exercise.jpg"},
            {"name": "Eat Dark chocolates", "image": "chocolates.jpg"}
        ])
        all_medicines.extend([
            {"name": "Pain reliever tablets", "image": "painkiller.jpg"}
        ])

    if "vomiting" in symptoms:
        diseases_found.append("Food Poisoning")
        all_home_remedies.extend([
            {"name": "Drink ORS", "image": "ors.jpg"},
            {"name": "Drink lemon water", "image": "lemon_water.jpg"}
        ])
        all_medicines.extend([
            {"name": "Anti-nausea medicine", "image": "medicine.jpg"}
        ])

    # If no disease matches
    if not diseases_found:
        diseases_found.append("Healthy")
        all_home_remedies.append({"name": "Maintain good health", "image": "healthy.jpg"})
        all_medicines.append({"name": "No medicine needed", "image": "healthy.jpg"})

    # Render result page
    return render_template("result.html",
                           diseases=diseases_found,
                           home_remedies=all_home_remedies,
                           medicines=all_medicines,
                           username=session['username'],
                           role=session['role'])

if __name__ == "__main__":
    app.run(debug=True)