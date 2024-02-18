from flask import Flask, render_template, request, redirect, url_for

#データベース使うためflask_sqlalchemyをインポート
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    todo = db.Column(db.String(128), nullable=False)

@app.route('/')
def index():
    data = ToDo.query.all()
    return render_template('todo.html',data=data)


# アイテム追加[create]
@app.route('/add',methods=['POST'])
def add():
    todo = request.form['todo']
    new_todo = ToDo(todo=todo)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))


# アイテム削除[delete]
@app.route('/del_todo/<int:id>')
def del_todo(id):
    del_data = ToDo.query.filter_by(id=id).first()
    db.session.delete(del_data)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # db.create_all()
    app.run()