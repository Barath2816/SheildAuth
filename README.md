
                    ShieldAuth
     Cybersecurity Toolkit Web Application


Project Name:
--------------
ShieldAuth

Project Description:
--------------------
ShieldAuth is a web-based cybersecurity toolkit developed using
Python Flask. The application provides multiple security tools
through a single, user-friendly interface. It is designed to help
users strengthen passwords, detect email breaches, encrypt files,
and identify phishing attempts while maintaining secure user
authentication.

Features:
---------
• Secure User Registration and Login
• Password Vulnerability Analyzer
• Email Breach Detection
• File Encryption & Decryption
• Phishing Detection
• Responsive Web Interface
• Cloud Deployment on Render

Technologies Used:
------------------
Backend:
- Python 3
- Flask

Frontend:
- HTML5
- CSS3
- JavaScript

Security:
- Flask-Bcrypt
- Cryptography (Fernet)
- SHA-1 Hashing
- Flask Sessions

Storage:
- JSON Files

Development Tools:
------------------
- Visual Studio Code
- Git & GitHub
- Render (Deployment)

Project Structure:
------------------

ShieldAuth/
│
├── app.py
├── requirements.txt
├── users.json
├── breach_hashes.json
├── templates/
├── static/
│   ├── css/
│   ├── javascript/
│   ├── images/
│   └── uploads/
├── encrypted/
├── decrypted/
└── README.txt

Modules:
--------

1. Authentication System
   - Secure registration and login
   - Password hashing using Bcrypt
   - Session management

2. Password Vulnerability Analyzer
   - Password strength analysis
   - Entropy calculation
   - Password complexity check
   - Cracking time estimation

3. Email Breach Detection
   - SHA-1 hashing
   - Email comparison against local breach database
   - Privacy-preserving breach detection

4. File Encryption & Decryption
   - Password-based encryption
   - Fernet symmetric encryption
   - Secure file download after encryption/decryption

5. Phishing Detection
   - Detects suspicious keywords
   - Identifies phishing indicators
   - Displays risk level and recommendations

Installation:
-------------

1. Clone the repository

   git clone https://github.com/<your-username>/ShieldAuth.git

2. Navigate to the project

   cd ShieldAuth

3. Install dependencies

   pip install -r requirements.txt

4. Run the application

   python app.py

5. Open your browser

   http://127.0.0.1:5000

Deployment:
-----------
Hosted using Render Cloud Platform.

Project Objectives:
-------------------
• Improve password security awareness
• Detect compromised email accounts
• Protect sensitive files using encryption
• Help users identify phishing attacks
• Demonstrate practical cybersecurity concepts

Future Enhancements:
--------------------
• AI-based phishing detection
• Multi-Factor Authentication (MFA)
• Database integration (MySQL/PostgreSQL)
• Real-time breach database API
• Audit logs and user activity tracking
• File sharing with expiration links
• Dashboard analytics
• Dark/Light theme support

References:
-----------
• Flask Documentation
  https://flask.palletsprojects.com

• Python Documentation
  https://docs.python.org

• Cryptography Library
  https://cryptography.io

• OWASP
  https://owasp.org

• Have I Been Pwned
  https://haveibeenpwned.com

Developer:
----------
Barath P

Project:
--------
Final Year B.Sc. Computer Science Project

=========================================================
ShieldAuth
Secure • Detect • Protect
=========================================================
