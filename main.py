from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from forms import ToDoForm, UpdateForm

app = Flask(__name__)
app.secret_key = "Solo Levelling"
bootstrap = Bootstrap5(app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class ToDoList(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    todo: Mapped[str] = mapped_column(String(300))
    date: Mapped[str] = mapped_column(String(15))


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    add_form = ToDoForm()

    if add_form.validate_on_submit():
        new_todo = ToDoList(todo=add_form.todo.data, date=add_form.date.data)
        db.session.add(new_todo)
        db.session.commit()

    with app.app_context():
        all_todo = db.session.execute(db.select(ToDoList)).scalars().all()

    return render_template("index.html", form=add_form, list=all_todo)


@app.route("/update/<tid>", methods=["GET", "POST"])
def update(tid):
    update_form = UpdateForm()
    if update_form.validate_on_submit():
        to_do = db.get_or_404(ToDoList, tid)
        to_do.todo = update_form.new_todo.data
        to_do.date = update_form.new_date.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("update.html", form=update_form)


@app.route("/delete/<tid>")
def delete(tid):
    todo_to_delete = db.get_or_404(ToDoList, tid)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=False)
