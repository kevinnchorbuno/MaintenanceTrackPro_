from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.fields import DateTimeLocalField

class MaintenanceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], default='medium')
    due_date = DateTimeLocalField('Due Date', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='scheduled')
    submit = SubmitField('Save Maintenance Task') 