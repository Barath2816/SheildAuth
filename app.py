import base64
import uuid
import json
import hashlib
import os
import re
from datetime import datetime

from urllib.parse import urlparse
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
from flask_bcrypt import Bcrypt
from cryptography.fernet import Fernet, InvalidToken

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "change_this_secret_key"
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ================= SETUP =================

shared_files = {}

os.makedirs("uploads", exist_ok=True)
os.makedirs("encrypted", exist_ok=True)
os.makedirs("decrypted", exist_ok=True)

# ================= USER SYSTEM =================

def load_users():
    try:
        with open("users.json","r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json","w") as f:
        json.dump(users,f,indent=4)

from functools import wraps
from flask import redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ---------- REGISTER ----------
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if username in users:
            return "User exists"

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        users[username] = hashed
        save_users(users)

        return redirect(url_for("login"))

    return render_template("register.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET","POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        users = load_users()

        # Check user exists
        if username in users:

            # Verify hashed password
            if bcrypt.check_password_hash(users[username], password):
                session["user"] = username
                return redirect(url_for("home"))

        # If anything fails
        error = "Invalid username or password ❌"

    return render_template("login.html", error=error)
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ================= PAGES =================

@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/password")
@login_required
def password():
    return render_template("password.html")

@app.route("/email")
@login_required
def email():
    return render_template("email.html")

@app.route("/file")
@login_required
def file():
    return render_template("file.html")

@app.route("/phishing")
@login_required
def phishing():
    return render_template("phishing.html")

# ================= PASSWORD ANALYZER =================

common_words = ["password","admin","123456","qwerty","letmein"]

@app.route("/analyze_password", methods=["POST"])
@login_required
def analyze_password():

    data = request.get_json()
    pwd = data["password"]
    length = len(pwd)

    if length < 8:
        strength = "Very Weak"
    elif length < 10:
        strength = "Weak"
    elif length < 12:
        strength = "Medium"
    else:
        strength = "Strong"

    complexity = sum([
        any(c.islower() for c in pwd),
        any(c.isupper() for c in pwd),
        any(c.isdigit() for c in pwd),
        any(not c.isalnum() for c in pwd)
    ])

    complexity_text = ["Very Poor","Poor","Good","Strong","Very Strong"][complexity]

    dictionary = "Looks Safe"
    for w in common_words:
        if w in pwd.lower():
            dictionary = "Contains Common Word ❌"
            break

    crack = "Years"
    if length < 6:
        crack = "Instant"
    elif length < 8:
        crack = "Minutes"
    elif length < 10:
        crack = "Hours"
    elif length < 12:
        crack = "Months"

    entropy = length * complexity * 2

    patterns = ["qwerty","asdf","1234","abcd"]
    pattern_warning = "No patterns detected"

    for p in patterns:
        if p in pwd.lower():
            pattern_warning = "Keyboard pattern detected ⚠️"

    repeat_warning = "Looks varied"
    if len(set(pwd)) <= 2:
        repeat_warning = "Too many repeating characters ⚠️"

    return jsonify({
        "strength": strength,
        "length": f"{length} Characters",
        "complexity": complexity_text,
        "dictionary": dictionary,
        "time": crack,
        "entropy": entropy,
        "pattern": pattern_warning,
        "repeat": repeat_warning
    })

# ================= EMAIL BREACH =================

@app.route("/check_email", methods=["POST"])
@login_required
def check_email():

    data = request.get_json()

    if not data or "email" not in data:
        return jsonify({"error": "Invalid request"}), 400

    email = data["email"].strip().lower()
    sha = hashlib.sha1(email.encode()).hexdigest().upper()

    try:
        with open("static/data/breach_hashes.json") as f:
            breaches = json.load(f)
    except:
        breaches = []

    for b in breaches:
        if b["hash"].upper() == sha:
            return jsonify({
                "breached": True,
                "risk_level": "HIGH",
                "risk_score": 85,
                "email_hash": sha,
                "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "recommendation": "Change your password immediately and enable 2FA.",
                **b
            })

    return jsonify({
        "breached": False,
        "risk_level": "LOW",
        "risk_score": 10,
        "email_hash": sha,
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "recommendation": "No action needed. Continue using strong passwords."
    })
# ================= FILE ENCRYPTION =================

def generate_key_from_password(password):
    key=hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

@app.route("/encrypt", methods=["POST"])
@login_required
def encrypt():

    file=request.files["file"]
    password=request.form["password"]

    cipher=Fernet(generate_key_from_password(password))

    filepath="uploads/"+file.filename
    file.save(filepath)

    with open(filepath,"rb") as f:
        data=f.read()

    encrypted_data=cipher.encrypt(data)

    unique_name=str(uuid.uuid4())+".enc"
    encrypted_path="encrypted/"+unique_name

    with open(encrypted_path,"wb") as f:
        f.write(encrypted_data)

    os.remove(filepath)

    share_id=str(uuid.uuid4())
    shared_files[share_id]=encrypted_path

    share_link=url_for("download_shared",file_id=share_id,_external=True)

    return render_template("encrypt_result.html", link=share_link)

@app.route("/share/<file_id>")
def download_shared(file_id):

    if file_id not in shared_files:
        return "Invalid link"

    return send_file(shared_files[file_id], as_attachment=True)

@app.route("/decrypt", methods=["POST"])
@login_required
def decrypt():

    file = request.files["file"]
    password = request.form["password"]

    cipher = Fernet(generate_key_from_password(password))

    filepath = "uploads/" + file.filename
    file.save(filepath)

    try:
        with open(filepath, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = cipher.decrypt(encrypted_data)

        decrypted_filename = "decrypted_" + file.filename.replace(".enc", "")
        decrypted_path = "decrypted/" + decrypted_filename

        with open(decrypted_path, "wb") as f:
            f.write(decrypted_data)

        os.remove(filepath)

        return send_file(decrypted_path, as_attachment=True)

    except InvalidToken:

        os.remove(filepath)

        return render_template(
            "file.html",
            decrypt_error="Invalid password or corrupted file ❌"
        )

# ================= PHISHING DETECTION =================

@app.route("/detect_phishing", methods=["POST"])
@login_required
def detect_phishing():

    data = request.get_json()
    content = data["content"].lower()

    score = 0
    reasons = []

    keywords = [
        "urgent",
        "verify",
        "click here",
        "bank",
        "password",
        "limited time",
        "account suspended",
        "confirm identity",
        "update account",
        "login now"
    ]

    # keyword detection
    for word in keywords:
        if word in content:
            score += 2
            reasons.append(f"Suspicious keyword: {word}")

    # url detection
    urls = re.findall(r'(https?://[^\s]+)', content)

    for url in urls:

        if url.startswith("http://"):
            score += 4
            reasons.append("Insecure HTTP link")

        if "login" in url or "verify" in url:
            score += 3
            reasons.append("Suspicious login/verify link")

    # risk level
    if score >= 8:
        level = "HIGH RISK"
    elif score >= 4:
        level = "MEDIUM RISK"
    else:
        level = "LOW RISK"

    return jsonify({
        "risk_level": level,
        "risk_score": score,
        "risk_percent": min(score*10,100),
        "reasons": reasons,
        "urls_found": urls
    })
# ================= START =================

if __name__ == "__main__":
    app.run(debug=True)