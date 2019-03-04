from flask_wtf import FlaskForm
from datetime import date
from wtforms import DateField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class VacationForm(FlaskForm):
	start = DateField('Vacation Start Date', validators=[DataRequired()], default=date.today)
	end = DateField('Vacation End Date', validators=[DataRequired()], default=date.today)
	submit = SubmitField('Submit')


	def validate_on_submit(self):
		result = super(VacationForm, self).validate()
		if (self.start.data > self.end.data):
			return False
		else: 
			return result
