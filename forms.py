from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired


class ToDoForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    todo = StringField("To Do", validators=[DataRequired()])
    add = SubmitField("Add")


class UpdateForm(FlaskForm):
    new_date = DateField("New Date", validators=[DataRequired()])
    new_todo = StringField("New To Do", validators=[DataRequired()])
    update = SubmitField("Update")
