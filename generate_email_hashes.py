import hashlib
import json
import os
import random

# Demo emails
emails = [
    "password@gmail.com",
    "barath2816@gmail.com",
    "john.smith@cybergate.com",
    "emma.wilson@techcore.io",
    "david.brown@securemail.net",
    "sophia.johnson@datashield.org",
    "michael.davis@netshield.com",
    "olivia.miller@cloudsecure.io",
    "daniel.taylor@alphatech.com",
    "ava.anderson@cybervault.net"
]

# Realistic breach examples
breaches = [
    ("LinkedIn Data Breach", "2012", "Email, Password"),
    ("Adobe Creative Cloud Breach", "2013", "Email, Password, Username"),
    ("Dropbox Security Incident", "2012", "Email, Password"),
    ("Yahoo Data Breach", "2016", "Email, Password, Phone Number"),
    ("Facebook Data Exposure", "2019", "Email, Phone Number"),
    ("Twitter Security Leak", "2020", "Email, Username"),
    ("Canva Data Breach", "2019", "Email, Username, Password"),
    ("MyFitnessPal Breach", "2018", "Email, Username, Password"),
    ("Quora Data Breach", "2018", "Email, Password, Username"),
]

file_path = "static/data/breach_hashes.json"

# Load existing data if file exists
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except:
            data = []
else:
    data = []

for email in emails:

    email_clean = email.strip().lower()

    hash_value = hashlib.sha1(email_clean.encode()).hexdigest().upper()

    breach = random.choice(breaches)

    data.append({
        "email": email_clean,
        "hash": hash_value,
        "breach": breach[0],
        "year": breach[1],
        "data": breach[2]
    })

# Save JSON
with open(file_path, "w") as f:
    json.dump(data, f, indent=4)

print("breach_hashes.json updated successfully!")