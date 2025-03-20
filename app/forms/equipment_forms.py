from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class EquipmentForm(FlaskForm):
    name = StringField('Equipment Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    image = FileField('Equipment Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only (jpg, png, jpeg)')
    ])
    health_score = FloatField('Health Score (0-100)', validators=[
        Optional(), 
        NumberRange(min=0, max=100, message='Health score must be between 0 and 100')
    ])
    submit = SubmitField('Save Equipment')

class EquipmentSearchForm(FlaskForm):
    search = StringField('Search Equipment', validators=[Optional()])
    submit = SubmitField('Search') 