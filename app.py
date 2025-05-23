from flask import Flask, render_template, request

from users import user

app = Flask(__name__)

app.register_blueprint(user, url_prefix='/')

@app.route('/')
def index():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)