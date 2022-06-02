from distutils.log import error
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


Todo.querry = db.session.query_property()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        taskContent = request.form["content"]
        newTask = Todo(content=taskContent)
        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            'there was a problem'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    taskDelete = Todo.query.get_or_404(id)
    try:
        db.session.delete(taskDelete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem deleting'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.querry.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was a problem with update'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
# oop sql
