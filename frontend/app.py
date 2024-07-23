from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

API_URL = "http://localhost:5000/api"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
        if response.status_code == 200:
            session['token'] = response.json()["access_token"]
            return redirect(url_for('notes'))
        else:
            return render_template('login.html', error="Login failed")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f"{API_URL}/auth/register", json={"username": username, "password": password})
        if response.status_code == 201:
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Registration failed")
    return render_template('register.html')


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    token = session.get('token')
    if not token:
        return redirect(url_for('login'))

    headers = {"Authorization": f"Bearer {token}"}

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        response = requests.post(f"{API_URL}/notes", json={"title": title, "content": content}, headers=headers)
        if response.status_code != 201:
            return render_template('notes.html', error="Failed to create note")

    response = requests.get(f"{API_URL}/notes", headers=headers)
    if response.status_code == 200:
        notes = response.json()
        return render_template('notes.html', notes=notes)
    else:
        return render_template('notes.html', error="Failed to load notes")


if __name__ == '__main__':
    app.run(debug=True, port=5001)
