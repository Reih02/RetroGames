from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


# sets a minimum and maximum length to the search query, as well as a condition
# that the search actually consists of something.
class SearchForm(FlaskForm):
    query = StringField('query', validators=[Length(min=2, max=35),
                                             DataRequired()])
    submit = SubmitField('🔍')
