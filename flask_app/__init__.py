from flask import Flask
app = Flask(__name__)

app.secret_key = 'password1234'
DATABASE= 'login_and_registration'