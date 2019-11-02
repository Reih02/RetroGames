from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# add max input
# makes user enter at least some data to complete a search
class SearchForm(FlaskForm):
    query = StringField('query', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('🔍')
