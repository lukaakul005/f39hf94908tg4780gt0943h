from flask import Flask, url_for, render_template, request, redirect, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
helo = 'sqlite:///users.db'



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
app.app_context().push()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Welcome!")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")
@app.route('/logout', methods=['GET', 'POST'])

def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))
@app.route('/home', methods=['GET'])
def home():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Hello!")




@app.route('/premium', methods=['GET', 'POST'])
def premium():
    if session.get('logged_in'):
        return render_template('premium.html')
    else:
        return render_template('login.html', message="Hello!")


@app.route('/rick-and-morty', methods=['GET'])
def rickandmorty():
    if session.get('logged_in'):
        return render_template('series/rickandmorty.html')
    else:
        return render_template('index.html', message="Hello!")





if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p4234324343"
    db.create_all()
    app.run(debug=True)
