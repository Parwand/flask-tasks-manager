from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


# create a task model for database
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/')
def index():  # put application's code here
    try:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template("index.html", tasks=tasks)
    except:
        return render_template("index.html")


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        task = request.form['task']
        new_task = Task(content=task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issues where adding your input"


if __name__ == '__main__':
    app.run()
    db.create_all()
