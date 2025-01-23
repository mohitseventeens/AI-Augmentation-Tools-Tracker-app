from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, URL, NumberRange

class ToolForm(FlaskForm):
    name = StringField('Tool Name', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Category', choices=[
        ('LLM', 'Large Language Model'),
        ('Agent', 'AI Agent'),
        ('Framework', 'Development Framework'),
        ('Utility', 'Utility Tool'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Description')
    url = StringField('URL', validators=[URL(), Length(max=200)])
    notes = TextAreaField('Notes')
    rating = IntegerField('Rating (1-5)', validators=[
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5')
    ])