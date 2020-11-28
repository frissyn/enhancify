from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import SubmitField
from wtforms import SelectField
from wtforms import TextAreaField

from wtforms.validators import DataRequired


class NewProject(FlaskForm):
    name = StringField("Project Name", validators=[DataRequired()])
    language = SelectField("Programming Language", choices=[("python", "Python-3")])

    content = TextAreaField("Paste Code", validators=[DataRequired()])
    submit = SubmitField("Create")
